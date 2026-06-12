from datetime import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _




class CustomUser(AbstractUser):
    avatar = models.ImageField(_('avatar'), upload_to="profile/avatars/")
    job_title = models.CharField(_('job_title'), max_length=150, blank=True, null=True)
    about_me = models.TextField(_('about_me'), blank=True, null=True)
    instagram_link = models.URLField(_('instagram_link'), blank=True, null=True)
    telegram_link = models.URLField(_('telegram_link'), blank=True, null=True)
    discord_link = models.URLField(_('discord_link'), blank=True, null=True)
    linkedin_link = models.URLField(_('linkedin_link'), blank=True, null=True)

    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)
    last_login = models.DateTimeField(_('last_login'), auto_now=True)

    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
