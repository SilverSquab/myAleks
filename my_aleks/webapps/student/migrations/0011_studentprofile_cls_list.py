# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2019-10-08 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_auto_20190916_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='cls_list',
            field=models.CharField(blank=True, default='[]', max_length=200, null=True),
        ),
    ]
