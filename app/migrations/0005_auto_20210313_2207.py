# Generated by Django 2.2.5 on 2021-03-13 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210313_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='face_id',
            field=models.IntegerField(default=0, verbose_name='人脸ID'),
        ),
    ]