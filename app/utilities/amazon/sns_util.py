import boto3
import random
import string

from loguru import logger
from datetime import datetime, timedelta

from app.utilities.redis import get_primary_client
from app.settings.configs import SNS_ACCESS_KEY, SNS_SECRET_KEY, AWS_REGION

class sns_control(object):
    def __init__(self):
        self.today = datetime.now()
        self.access_key = SNS_ACCESS_KEY
        self.secret_key = SNS_SECRET_KEY
        self.aws_region = AWS_REGION

    def connect_to_sns(self):
        sns_session = None
        try:
            session = boto3.Session(
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.aws_region
            )
            sns_session = session.client('sns')
            return sns_session
        except Exception as e:
            logger.error(f"connect_to_sns : {e}")
            sns_session = e

        return sns_session

    def get_redis_client(self):
        redis_client = get_primary_client()
        return redis_client

    def generate_otp(self):
        length = 6
        characters = string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def store_otp(self, mobile_phone_number, otp):
        redis_client = self.get_redis_client()
        redis_key = f"otp:{mobile_phone_number}"
        ttl_seconds = int(timedelta(minutes=10).total_seconds())
        redis_client.setex(redis_key, ttl_seconds, otp)

    def check_otp(self, mobile_phone_number, otp):
        try:
            redis_client = self.get_redis_client()
            redis_key = f"otp:{mobile_phone_number}"
            stored_otp = redis_client.get(redis_key)

            if stored_otp is None:
                return None, {"error_code": "01","msg": "otp timeout"}
            if stored_otp.decode() != otp:
                return None, {"error_code": "02","msg": "otp_invalid"}

            return redis_client, {"success_code": "01", "msg": "otp_valid"}
        except Exception as e:
            logger.error(e)
            redis_client.delete(redis_key)
            return {"error_code": "03","msg": f"otp_invalid : {e}"}
    
    def send_mobile_phone_number(self, mobile_phone_number):
        redis_client = self.get_redis_client()
        redis_key = f"otp:{mobile_phone_number}"
        stored_otp = redis_client.get(redis_key)
        if stored_otp is not None:
            remaining_time = redis_client.ttl(redis_key)
            if remaining_time >= 540:
                remaining_time_not_over = {
                    "error_code": "03",
                    "msg": f"OTP for mobile_phone_number {mobile_phone_number} already exists and has {remaining_time} seconds remaining"
                }

                return remaining_time_not_over
            else:
                redis_client.delete(redis_key)

        otp = self.generate_otp()
        body = f"Your OTP is: {otp}, OTP 10 minutes remaining"

        sns_session = self.connect_to_sns()
        if isinstance(sns_session, Exception):
            return {
                    "error_server": "04",
                    "msg": f"sns server can't connected : {sns_session}"
                }

        try:
            response = sns_session.publish(
                PhoneNumber=mobile_phone_number,
                Message=body,
                Subject='Dedee'
            )
            message_id = response['MessageId']

            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                result = {
                    "success_code": "01",
                    "msg": f"OTP for mobile_phone_number {mobile_phone_number} has 10 minutes remaining"
                }
            else:
                return {
                    "error_server": "05",
                    "msg": f"Failed to send SMS message! : {mobile_phone_number}"
                }

        except Exception as e:
            logger.error(e)
            return {
                    "error_server": "06",
                    "msg": f"sns server can't sending : {e}"
                }
        
        self.store_otp(mobile_phone_number, otp)
        return result

