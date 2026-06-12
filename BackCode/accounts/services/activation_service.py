from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.html import strip_tags


def send_activation_register_email(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"{settings.FRONTEND_URL}/activate/{uid}/{token}/"

    user_display = user.get_full_name() or user.username

    html_content = render_to_string('emails/activation_email.html', {
        'title': 'فعال‌سازی حساب کاربری در Ariaskill',
        'user_display': user_display,
        'message': 'از پیوستن شما به خانواده بزرگ Ariaskill خوشحالیم. برای فعال‌سازی حساب کاربری و شروع ساخت رزومه حرفه‌ای، روی دکمه زیر کلیک کنید.',
        'button_text': '✅ فعال‌سازی حساب',
        'button_link': activation_link,
        'extra_note': '🔒 لینک فعال‌سازی به مدت <strong>۲۴ ساعت</strong> معتبر است.<br>✨ پس از فعالسازی می‌توانید رزومه خود را ساخته، به هزاران فرصت شغلی دسترسی پیدا کنید و توسط کارفرمایان دیده شوید.<br>❓ اگر درخواست فعال‌سازی نداده‌اید، لطفاً این ایمیل را نادیده بگیرید.',
        'site_url': settings.FRONTEND_URL,
    })

    plain_message = strip_tags(html_content)

    send_mail(
        subject=f"فعال‌سازی حساب در Ariaskill - خوش آمدید {user_display}",
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_content,
        fail_silently=False,
    )


def send_activation_change_pass_email(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_link = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"

    user_display = user.get_full_name() or user.username

    html_content = render_to_string('emails/reset_password_email.html', {
        'title': 'بازیابی رمز عبور Ariaskill',
        'user_display': user_display,
        'message': 'درخواست بازنشانی رمز عبور برای حساب شما ثبت شده است. اگر این درخواست را شما داده‌اید، با کلیک روی دکمه زیر رمز جدیدی انتخاب کنید.',
        'button_text': '🔄 بازنشانی رمز عبور',
        'button_link': reset_link,
        'extra_note': '⚠️ لینک بازنشانی فقط <strong>یک بار</strong> قابل استفاده است و تا <strong>۲۴ ساعت</strong> اعتبار دارد.<br>🔐 اگر شما درخواست بازنشانی نداده‌اید، کسی نمی‌تواند بدون دسترسی به ایمیل شما رمز را تغییر دهد. با خیال راحت این ایمیل را حذف کنید.<br>🛡️ برای امنیت بیشتر، پس از ورود رمز قوی انتخاب کنید.',
        'site_url': settings.FRONTEND_URL,
    })

    plain_message = strip_tags(html_content)

    send_mail(
        subject=f"بازیابی رمز عبور Ariaskill - درخواست {user_display}",
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_content,
        fail_silently=False,
    )
    return uid, token