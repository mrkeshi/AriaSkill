# Migration to remove view_count, download_count, last_download from Project

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_comment_default_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='view_count',
        ),
        migrations.RemoveField(
            model_name='project',
            name='download_count',
        ),
        migrations.RemoveField(
            model_name='project',
            name='last_download',
        ),
    ]
