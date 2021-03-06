# Generated by Django 2.1.7 on 2019-03-06 22:22

import courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0024_auto_20190305_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_image',
            field=models.ImageField(default='course/default_image/course_default.jpg', max_length=500, upload_to=courses.models.get_upload_course_image_path, verbose_name='课程图片'),
        ),
    ]
