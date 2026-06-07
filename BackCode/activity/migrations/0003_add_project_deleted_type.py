from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_new_activity_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='type',
            field=models.CharField(
                choices=[
                    ('login_success', 'Login Success'),
                    ('login_failed', 'Login Failed'),
                    ('project_published', 'Project Published'),
                    ('project_created', 'Project Created'),
                    ('project_updated', 'Project Updated'),
                    ('project_deleted', 'Project Deleted'),
                    ('password_changed', 'Password Changed'),
                    ('project_documentation_downloaded', 'Project Documentation Downloaded'),
                    ('external_project_comment_created', 'External Project Comment Created'),
                    ('comment_created', 'Comment Created'),
                ],
                max_length=80,
            ),
        ),
    ]
