# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-15 07:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wbot', '0002_auto_20171214_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='startedOn',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2017, 12, 15, 7, 6, 35, 296939, tzinfo=utc)),
            preserve_default=False,
        ),
    ]