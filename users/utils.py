from random import choice
from django.conf import settings
from .sms_utils import SendSMS

eskiz_conf = SendSMS(
    **settings.SMS_CONFIG
)

def generate_otp() -> str:
    return ''.join(choice('0123456789') for _ in range(4))

    
def send_sms(phone: str) -> str:
    key = generate_otp() # this is the OTP
    message = f"Pitak...\nSizning bir martalik kirish kodingiz {key}" # Write your own message here
    if phone and message:
        try:
            if settings.SMS_ENABLED:
                eskiz_conf.send_sms(message=message, phone=phone)
            # print("OTP:", key)
            return key
        except Exception as e:
            raise Exception("Can not send_sms")
    else:
        raise Exception("Phone number or message is missing")