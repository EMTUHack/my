# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-03 19:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hackers', '0011_remove_hacker_waitlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='hacker',
            name='waitlist_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 3, 19, 9, 21, 695654, tzinfo=utc)),
            preserve_default=False,
        ),
    ]