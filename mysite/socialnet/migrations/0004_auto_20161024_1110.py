# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 11:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnet', '0003_auto_20161024_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='avatar',
            field=models.ImageField(upload_to=b'/home/user/Documents/404/CMPUT404Project/mysite/static'),
        ),
    ]
