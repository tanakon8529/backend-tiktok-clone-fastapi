import smtplib
import random
import string
import time

from loguru import logger
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE

from app.utilities.redis import get_primary_client
from app.settings.configs import SES_USERNAME, SES_PASSWORD, CF_EMAIL_SENDER, SES_ENDPOINT

class ses_control(object):
    def __init__(self):
        self.today = datetime.now()
        self.username = SES_USERNAME
        self.password = SES_PASSWORD
        self.sender_email = CF_EMAIL_SENDER
        self.endpoint = SES_ENDPOINT

    def connect_to_ses(self):
        smtp_server = None
        try:
            smtp_server = smtplib.SMTP(self.endpoint, 587)
            smtp_server.ehlo()
            smtp_server.starttls()
            smtp_server.ehlo()
            smtp_server.login(self.username, self.password)
        except Exception as e:
            logger.error(f"connect_to_ses : {e}")
            smtp_server = e

        return smtp_server

    def get_redis_client(self):
        redis_client = get_primary_client()
        return redis_client

    def generate_otp(self):
        length = 6
        characters = string.digits
        return ''.join(random.choice(characters) for _ in range(length))
 
    def store_otp(self, email, otp):
        redis_client = self.get_redis_client()
        redis_key = f"otp:{email}"
        ttl_seconds = int(timedelta(minutes=10).total_seconds())
        redis_client.setex(redis_key, ttl_seconds, otp)

    def check_otp(self, email, otp):
        try:
            redis_client = self.get_redis_client()
            redis_key = f"otp:{email}"
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

    
    def send_email(self, email):
        redis_client = self.get_redis_client()
        redis_key = f"otp:{email}"
        stored_otp = redis_client.get(redis_key)
        if stored_otp is not None:
            remaining_time = redis_client.ttl(redis_key)
            if remaining_time >= 540:
                remaining_time_not_over = {
                    "error_code": "01",
                    "msg": f"OTP for email {email} already exists and has {remaining_time} seconds remaining"
                }

                return remaining_time_not_over
            else:
                redis_client.delete(redis_key)
        otp = self.generate_otp()
        subject = "Your OTP"
        body = f"Your OTP is: {otp}, OTP 10 minutes remaining"

        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = COMMASPACE.join([email])
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        timeout = time.time() + 5  # set timeout to 5 seconds
        while time.time() < timeout:
            smtp_server = self.connect_to_ses()
            if isinstance(smtp_server, Exception):
                logger.error(smtp_server)
                time.sleep(1)  # sleep for 1 second before trying again
                continue
            else:
                break

        if isinstance(smtp_server, Exception):
            logger.error(smtp_server)
            smtp_server.quit()
            return {
                "error_server": "02",
                "msg": f"smtp server can't connected : {smtp_server}"
            }

        result = {
                    "error_server": "03",
                    "msg": f"smtp server can't sending"
                }
        try:
            smtp_server.sendmail(self.sender_email, [email], message.as_string())
            result = {
                "success_code": "01",
                "msg": f"OTP for email {email} has 10 minutes remaining"
            }
            
        except Exception as e:
            logger.error(e)
            result = {
                    "error_server": "04",
                    "msg": f"smtp server can't sending : {e}"
                }
        
        self.store_otp(email, otp)
        smtp_server.quit()
        return result

