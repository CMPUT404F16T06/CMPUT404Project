# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-21 04:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnet', '0025_auto_20161121_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='visibility',
            field=models.BooleanField(default=True),
        ),
    ]
