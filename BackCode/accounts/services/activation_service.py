from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_activation_register_email(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # activation_link = f"{settings.FRONTEND_URL}/activate/{uid}/{token}/"

    print(f"{uid} \n {token}")

    # send_mail(
    #     subject="فعال‌سازی حساب کاربری",
    #     message=f"برای فعال‌سازی حساب روی لینک کلیک کنید:\n{activation_link}",
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     recipient_list=[user.email],
    # )


def send_activation_change_pass_email(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # reset_link = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"
    #
    # send_mail(
    #     subject='ریست کردن رمزعبور',
    #     message=f'\n {reset_link}برای ریست پسورد لینک کنید:',
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     recipient_list=[user.email],
    # )
    return uid, token