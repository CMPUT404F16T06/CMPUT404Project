# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-20 23:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnet', '0019_auto_20161120_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content_type',
            field=models.CharField(choices=[('text/plain', 'text/plain'), ('text/markdown', 'text/markdown')], default='text/plain', max_length=15),
        ),
        migrations.AlterField(
            model_name='post',
            name='content_type',
            field=models.CharField(choices=[('text/plain', 'text/plain'), ('text/markdown', 'text/markdown')], default='text/plain', max_length=15),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.CharField(default=None, max_length=40),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default=None, max_length=40),
        ),
    ]
