# Generated by Django 5.1.5 on 2025-01-22 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_complementaryactivity_certificateid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='file',
            field=models.FileField(upload_to='files/certificates/'),
        ),
        migrations.AlterField(
            model_name='event',
            name='picture',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='files/images/event/'),
        ),
        migrations.AlterField(
            model_name='principal',
            name='picture',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='files/images/principal/'),
        ),
        migrations.AlterField(
            model_name='professor',
            name='picture',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='files/images/professor/'),
        ),
        migrations.AlterField(
            model_name='student',
            name='picture',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='files/images/student/'),
        ),
    ]
