# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2019-10-28 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_auto_20190822_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='cls',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
