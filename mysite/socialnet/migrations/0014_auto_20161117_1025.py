# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-17 10:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnet', '0013_auto_20161117_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='following',
            field=models.ManyToManyField(blank=True, to='socialnet.Author'),
        ),
    ]