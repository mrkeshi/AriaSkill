from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_alter_notification_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BroadcastLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title',          models.CharField(max_length=180)),
                ('message',        models.TextField()),
                ('sent_to_count',  models.PositiveIntegerField(default=0, help_text='Number of users who received this broadcast.')),
                ('sent_at',        models.DateTimeField(auto_now_add=True)),
                ('sent_by', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='broadcast_logs',
                    to=settings.AUTH_USER_MODEL,
                    help_text='Admin who sent the broadcast.',
                )),
            ],
            options={
                'ordering': ['-sent_at'],
            },
        ),
        migrations.AddIndex(
            model_name='broadcastlog',
            index=models.Index(fields=['-sent_at'], name='broadcastlog_sent_at_idx'),
        ),
    ]
