# Generated by Django 5.1.5 on 2025-01-22 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_hourtype_activitytype_event_certificate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='path',
        ),
        migrations.AddField(
            model_name='certificate',
            name='file',
            field=models.FileField(default='', upload_to='certificate/'),
            preserve_default=False,
        ),
    ]
