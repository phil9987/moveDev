# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moveDevServer', '0008_userpooledtimestamp_steps'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpooledtimestamp',
            name='pool_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
