# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 17:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlayBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currstate', models.CommaSeparatedIntegerField(max_length=1000)),
                ('player1_id', models.CharField(max_length=100)),
                ('player2_id', models.CharField(max_length=100)),
                ('game_id', models.CharField(max_length=100)),
            ],
        ),
    ]
