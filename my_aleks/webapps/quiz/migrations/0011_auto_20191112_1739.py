# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2019-11-12 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_question_authenticated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='authenticated',
            field=models.CharField(db_index=True, default='U', max_length=5),
        ),
    ]