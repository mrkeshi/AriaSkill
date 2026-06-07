import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0003_alter_comment_status_alter_project_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('login_success', 'Login Success'), ('login_failed', 'Login Failed'), ('project_published', 'Project Published'), ('password_changed', 'Password Changed'), ('project_documentation_downloaded', 'Project Documentation Downloaded'), ('external_project_comment_created', 'External Project Comment Created')], max_length=80)),
                ('title', models.CharField(max_length=180)),
                ('description', models.TextField()),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('is_seen', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('related_project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activities', to='projects.project')),
                ('related_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_activities', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['is_seen', '-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['user', 'is_seen', '-created_at'], name='activity_feed_idx'),
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['user', 'type', '-created_at'], name='activity_type_idx'),
        ),
        migrations.AddIndex(
            model_name='activity',
            index=models.Index(fields=['user', 'deleted_at'], name='activity_deleted_idx'),
        ),
    ]
