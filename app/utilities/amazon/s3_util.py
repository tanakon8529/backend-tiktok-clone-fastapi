import boto3, hashlib, magic
import io, math, subprocess

from PIL import Image
from loguru import logger
from datetime import datetime, timedelta

from app.settings.configs import AWS_REGION, AWS_KEY_ID, AWS_KEY_SECRET, BUCKET_NAME_CLIENT_IMAGES, BUCKET_NAME_CLIENT_CLIPS

class s3_control(object):
    def __init__(self):
        self.today = datetime.now()
        self.region_name = AWS_REGION
        self.aws_access_key_id = AWS_KEY_ID
        self.aws_secret_access_key = AWS_KEY_SECRET
        self.bucket_name_images = BUCKET_NAME_CLIENT_IMAGES
        self.bucket_name_clips = BUCKET_NAME_CLIENT_CLIPS
        self.file_name_image = "image"
        self.file_name_clip = "clip"
        self.max_image_size = 3000000 # 3MB in bytes
        self.max_video_size = 100 * 1024 * 1024 # 100MB in bytes
        self.expire_day = 1095 # 3 year
        self.magic = magic.Magic(mime=True)

    def aws_s3_connect(self):
        try:
            s3_resource = boto3.client(
                service_name = 's3',
                region_name = self.region_name,
                aws_access_key_id = self.aws_access_key_id,
                aws_secret_access_key = self.aws_secret_access_key
            )
            return s3_resource
        except Exception as e:
            logger.error(f"aws_s3_connect : {e}")

    ## using for list all object in your Bucket on AWS S3 ###
    def list_objects_in_s3(self, aws_session):
        my_bucket = aws_session.list_objects(Bucket=self.bucket_name_images)['Contents']
        ## loop print
        # for my_object in my_bucket:
        #     print(my_object)
        return my_bucket

    ## using for get object in your Bucket on AWS S3 ###
    def get_objects_in_s3_by_key(self, aws_session, file_key_s3):
        my_object = aws_session.get_object(Bucket=self.bucket_name_images, Key=file_key_s3)
        return my_object
    
    def get_video_resolution(self, url):
        command = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 {url}'
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, _ = result.communicate()
        resolution = output.decode().strip()
        return resolution

    def limit_video(self, file_size_kb):
        result = "PASS"
        try:
            # Check the file size of the video
            if file_size_kb > self.max_video_size:
                result = {"error_server": "01", "msg": "Video file size is too large (maximum 100MB)"}
        except Exception as e:
            logger.error(e)
            result = {"error_server": "02", "msg": f"Invalid video file : {e}"}

        return result
    
    def limit_image(self, file_for_upload, file_size_kb):
        img = Image.open(file_for_upload)
        width, height = img.size
        ratio = width / height
        new_width = int(math.sqrt(3000 * ratio))
        new_height = int(new_width / ratio)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        file_for_upload = io.BytesIO()
        img.save(file_for_upload, format='JPEG', quality=90)
        file_for_upload.seek(0)
        size_file_text = file_for_upload.read()
        file_size_kb = len(size_file_text)

        return file_for_upload, file_size_kb
    
    def encode_file_name(self, file_name):
        file_name_encyp = int.from_bytes(file_name.encode('utf-8'), byteorder='big')
        return str(file_name_encyp)[:10]

    # if you need, decode original file_name
    # def decode_file_name(self, file_name_encyp, file_name):
    #     file_name_deco = int.to_bytes(file_name_encyp, length=len(file_name), byteorder='big').decode('utf-8')
    #     return file_name_deco
    ############################ UPLOAD IMAGES ############################
    #######################################################################
        
    def upload_images_profile_attachment(self, today, payload, files, aws_session):
        logger.debug(files)

        file_url_s3 = None
        response = None
        result_pack = []

        for file in files:
            file_for_upload = file.file
            file_name_origin = file.filename
            file_name = self.file_name_image + "_" + today.strftime("%Y-%m-%d_%H-%M-%S") + "_" + self.encode_file_name(file_name_origin)
            string_for_key = file_name

            size_file_text = file.file.read()
            file_size_kb = len(size_file_text)

            if file_size_kb > self.max_image_size:
                file_for_upload, file_size_kb = self.limit_image(file_for_upload, file_size_kb)
                if file_size_kb > self.max_image_size:
                    return {"error_server": "01", "msg": "Invalid Image file size"}

            file_type = magic.from_buffer(file_for_upload.read(), mime=True)
            profile_name_uuid = payload.profile_name_uuid

            result = {}
            expire_date = today + timedelta(days=self.expire_day)
            try:
                file_key_s3 = hashlib.md5(string_for_key.encode()).hexdigest()
                expireduration = ((expire_date) - today).total_seconds()
                file_for_upload.seek(0, 0)
                response = aws_session.put_object(
                    ACL = "public-read",
                    Body = file_for_upload,
                    Bucket = self.bucket_name_images,
                    Key = file_key_s3,
                    #### for read jpg on browser ####
                    ContentType = 'image/jpg'
                    #### for download file by url ####
                    # ContentDisposition = 'attachment; filename=\"' + file_name + '\"'
                )
                file_url_s3 = aws_session.generate_presigned_url('get_object', 
                                                         Params = {'Bucket': self.bucket_name_images, 
                                                                   'Key': file_key_s3
                                                                   }, 
                                                         ExpiresIn=expireduration)
                result = {
                    "file_name" : file_name,
                    "file_type" : file_type,
                    "file_url_s3" : file_url_s3,
                    "file_size_kb": file_size_kb,
                    "file_key_s3" : file_key_s3,
                    "file_url_expire_date_s3" : expire_date,
                    "profile_name_uuid" : profile_name_uuid,
                    "status_upload" : True
                }

            except Exception as e:
                logger.error(f"aws_s3_connect : {e}")
                if response:
                    logger.error(f"aws_s3_response : {response}")
                result = {
                    "file_name" : file_name,
                    "profile_name_uuid" : profile_name_uuid,
                    "status_upload" : False,
                    "detail" : e
                }

            result_pack.append(result)
        
        return result_pack
    
    def upload_images_group_attachment(self, today, payload, files, aws_session):
        logger.debug(files)

        file_url_s3 = None
        response = None
        result_pack = []

        for file in files:
            file_for_upload = file.file
            file_name_origin = file.filename
            file_name = self.file_name_image + "_" + today.strftime("%Y-%m-%d_%H-%M-%S") + "_" + self.encode_file_name(file_name_origin)
            string_for_key = file_name

            size_file_text = file.file.read()
            file_size_kb = len(size_file_text)
            
            if file_size_kb > self.max_image_size:
                file_for_upload, file_size_kb = self.limit_image(file_for_upload, file_size_kb)
                if file_size_kb > self.max_image_size:
                    return {"error_server": "01", "msg": "Invalid Image file size"}

            file_type = magic.from_buffer(file_for_upload.read(), mime=True)
            group_name_uuid = payload["group_name_uuid"]

            result = {}
            expire_date = today + timedelta(days=self.expire_day)
            string_for_key = ''.join([file_name, today.strftime("%Y-%m-%d %H-%M-%S")])
            try:
                file_key_s3 = hashlib.md5(string_for_key.encode()).hexdigest()
                expireduration = ((expire_date) - today).total_seconds()
                file_for_upload.seek(0, 0)
                response = aws_session.put_object(
                    ACL = "public-read",
                    Body = file_for_upload,
                    Bucket = self.bucket_name_images,
                    Key = file_key_s3,
                    #### for read jpg on browser ####
                    ContentType = 'image/jpg'
                    #### for download file by url ####
                    # ContentDisposition = 'attachment; filename=\"' + file_name + '\"'
                )
                file_url_s3 = aws_session.generate_presigned_url('get_object', 
                                                         Params = {'Bucket': self.bucket_name_images, 
                                                                   'Key': file_key_s3
                                                                   }, 
                                                         ExpiresIn=expireduration)
                result = {
                    "file_name" : file_name,
                    "file_type" : file_type,
                    "file_url_s3" : file_url_s3,
                    "file_size_kb": file_size_kb,
                    "file_key_s3" : file_key_s3,
                    "file_url_expire_date_s3" : expire_date,
                    "group_name_uuid" : group_name_uuid,
                    "status_upload" : True
                }

            except Exception as e:
                logger.error(f"aws_s3_connect : {e}")
                if response:
                    logger.error(f"aws_s3_response : {response}")
                result = {
                    "file_name" : file_name,
                    "group_name_uuid" : group_name_uuid,
                    "status_upload" : False,
                    "detail" : e
                }

            result_pack.append(result)
        
        return result_pack
    
    ############################ UPLOAD CLIPS ############################
    ######################################################################
    def upload_clips_profile_attachment(self, today, payload, files, aws_session):
        logger.debug(files)

        file_url_s3 = None
        response = None
        result_pack = []

        """
                    FOR TEST
        total_file_size_kb = 0
        """

        for file in files:
            # Check if the video file meets the resolution and size requirements
            file_for_upload = file.file
            file_name_origin = file.filename
            file_name = self.file_name_clip + "_" + today.strftime("%Y-%m-%d_%H-%M-%S") + "_" + self.encode_file_name(file_name_origin)
            string_for_key = file_name

            size_file_text = file.file.read()
            file_size_kb = len(size_file_text)
            reduce_file = self.limit_video(file_size_kb)
            if "error_server" in reduce_file:
                return reduce_file

            file_type = magic.from_buffer(file_for_upload.read(), mime=True)
            profile_name_uuid = payload.profile_name_uuid

            result = {}
            expire_date = today + timedelta(days=self.expire_day)
            string_for_key = ''.join([file_name, today.strftime("%Y-%m-%d %H-%M-%S")])
            try:
                file_key_s3 = hashlib.md5(string_for_key.encode()).hexdigest()
                expireduration = ((expire_date) - today).total_seconds()
                file_for_upload.seek(0, 0)
                response = aws_session.put_object(
                    ACL = "public-read",
                    Body = file_for_upload,
                    Bucket = self.bucket_name_clips,
                    Key = file_key_s3,
                    ContentType = 'video/mp4'
                )
                file_url_s3 = aws_session.generate_presigned_url('get_object', 
                                                         Params = {'Bucket': self.bucket_name_clips, 
                                                                   'Key': file_key_s3
                                                                   }, 
                                                         ExpiresIn=expireduration)
                result = {
                    "file_name" : file_name,
                    "file_type" : file_type,
                    "file_url_s3" : file_url_s3,
                    "file_size_kb": file_size_kb,
                    "file_key_s3" : file_key_s3,
                    "file_url_expire_date_s3" : expire_date,
                    "profile_name_uuid" : profile_name_uuid,
                    "status_upload" : True
                }

                """
                    FOR TEST
                
                # total_file_size_kb += file_size_kb
                # video_resolution = self.get_video_resolution(file_url_s3)
                # logger.debug(f"video_resolution : {video_resolution}")

                """
            except Exception as e:
                logger.error(f"aws_s3_connect : {e}")
                if response:
                    logger.error(f"aws_s3_response : {response}")
                result = {
                    "file_name" : file_name,
                    "profile_name_uuid" : profile_name_uuid,
                    "status_upload" : False,
                    "detail" : e
                }

            result_pack.append(result)
        """
                    FOR TEST
        # logger.debug(f"total_file_size_kb : {total_file_size_kb} KB")
        """
        return result_pack
    
    def upload_clips_group_attachment(self, today, payload, files, aws_session):
        logger.debug(files)

        file_url_s3 = None
        response = None
        result_pack = []

        for file in files:
            # Check if the video file meets the resolution and size requirements
            file_for_upload = file.file
            file_name_origin = file.filename
            file_name = self.file_name_clip + "_" + today.strftime("%Y-%m-%d_%H-%M-%S") + "_" + self.encode_file_name(file_name_origin)
            string_for_key = file_name

            size_file_text = file.file.read()
            file_size_kb = len(size_file_text)
            reduce_file = self.limit_video(file_size_kb)
            if "error_server" in reduce_file:
                return reduce_file
            
            file_type = magic.from_buffer(file_for_upload.read(), mime=True)
            group_name_uuid = payload.group_name_uuid

            result = {}
            expire_date = today + timedelta(days=self.expire_day)
            string_for_key = ''.join([file_name, today.strftime("%Y-%m-%d %H-%M-%S")])
            try:
                file_key_s3 = hashlib.md5(string_for_key.encode()).hexdigest()
                expireduration = ((expire_date) - today).total_seconds()
                file_for_upload.seek(0, 0)
                response = aws_session.put_object(
                    ACL = "public-read",
                    Body = file_for_upload,
                    Bucket = self.bucket_name_clips,
                    Key = file_key_s3,
                    ContentType = 'video/mp4'
                )
                file_url_s3 = aws_session.generate_presigned_url('get_object', 
                                                         Params = {'Bucket': self.bucket_name_clips, 
                                                                   'Key': file_key_s3
                                                                   }, 
                                                         ExpiresIn=expireduration)
                result = {
                    "file_name" : file_name,
                    "file_type" : file_type,
                    "file_url_s3" : file_url_s3,
                    "file_size_kb": file_size_kb,
                    "file_key_s3" : file_key_s3,
                    "file_url_expire_date_s3" : expire_date,
                    "group_name_uuid" : group_name_uuid,
                    "status_upload" : True
                }

            except Exception as e:
                logger.error(f"aws_s3_connect : {e}")
                if response:
                    logger.error(f"aws_s3_response : {response}")
                result = {
                    "file_name" : file_name,
                    "group_name_uuid" : group_name_uuid,
                    "status_upload" : False,
                    "detail" : e
                }

            result_pack.append(result)
        
        return result_pack

    def delete_object_s3_by_key(self, file_detail, file_type, aws_session):
        logger.debug(file_detail)
        file_key_s3 = file_detail.file_key_s3
        if file_type == True:
            bucket_name = self.bucket_name_images
        elif file_type == False:
            bucket_name = self.bucket_name_clips

        try:
            aws_session.delete_object(Bucket=bucket_name, Key=file_key_s3)
            result = {
                "file_name" : file_detail.file_name,
                "file_key_s3" : file_key_s3,
                "status_delete" : True
            }
        except Exception as e:
            logger.error(f"aws_s3_connect : {e}")
            result = {
                "file_name" : file_detail.file_name,
                "file_key_s3" : file_key_s3,
                "status_upload" : False,
                "detail" : e
            }

        return result
