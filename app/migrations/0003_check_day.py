# Generated by Django 2.2.5 on 2021-03-13 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210313_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='day',
            field=models.DateField(default="2021-01-01", verbose_name='签到日'),
            preserve_default=False,
        ),
    ]