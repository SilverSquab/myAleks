# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2019-10-30 09:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_cls_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='phone',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]