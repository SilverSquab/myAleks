# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2019-10-25 13:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_auto_20191025_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentquizrecord',
            name='student',
        ),
    ]