# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2019-09-12 06:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_quiz_quiz_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizrecord',
            name='cls',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.Cls'),
        ),
    ]