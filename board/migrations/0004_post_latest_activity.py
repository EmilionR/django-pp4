# Generated by Django 4.2.9 on 2024-02-21 14:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_like_like_like_post_or_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='latest_activity',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
