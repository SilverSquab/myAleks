# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2019-08-07 02:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import webapps.knowledge_space.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorReason',
            fields=[
                ('id', models.CharField(default=webapps.knowledge_space.models.get_uuid4, max_length=20, primary_key=True, serialize=False)),
                ('descritpion', models.TextField(max_length=200)),
                ('info', models.TextField(blank=True, max_length=1000, null=True)),
                ('weight', models.FloatField(default=1.0)),
            ],
        ),
        migrations.CreateModel(
            name='KnowledgeGraph',
            fields=[
                ('id', models.CharField(default=webapps.knowledge_space.models.get_uuid4, max_length=20, primary_key=True, serialize=False)),
                ('uri', models.CharField(default='None', max_length=100)),
                ('subject', models.CharField(db_index=True, max_length=20)),
                ('description', models.TextField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='KnowledgeGraphEdge',
            fields=[
                ('id', models.CharField(default=webapps.knowledge_space.models.get_uuid4, max_length=20, primary_key=True, serialize=False)),
                ('weight', models.FloatField(default=1.0)),
            ],
        ),
        migrations.CreateModel(
            name='KnowledgeNode',
            fields=[
                ('id', models.CharField(default=webapps.knowledge_space.models.get_uuid4, max_length=20, primary_key=True, serialize=False)),
                ('description', models.TextField(max_length=200)),
                ('title', models.TextField(blank=True, max_length=200, null=True)),
                ('graph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge_space.KnowledgeGraph')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('chinese_name', models.CharField(blank=True, max_length=40, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='knowledgegraphedge',
            name='predecessor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='successors', to='knowledge_space.KnowledgeNode'),
        ),
        migrations.AddField(
            model_name='knowledgegraphedge',
            name='successor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predecessors', to='knowledge_space.KnowledgeNode'),
        ),
        migrations.AddField(
            model_name='errorreason',
            name='knowledge_node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge_space.KnowledgeNode'),
        ),
    ]
