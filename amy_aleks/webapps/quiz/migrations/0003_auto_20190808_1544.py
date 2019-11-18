# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2019-08-08 07:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20190807_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizRecordPaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_uri', models.CharField(max_length=150)),
                ('html_uri', models.CharField(max_length=150)),
                ('quiz_record', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.QuizRecord')),
            ],
        ),
        migrations.AlterField(
            model_name='question',
            name='uploader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions_uploaded', to=settings.AUTH_USER_MODEL),
        ),
    ]