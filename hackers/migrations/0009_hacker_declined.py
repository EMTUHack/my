# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-02 05:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackers', '0008_auto_20180302_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='hacker',
            name='declined',
            field=models.BooleanField(default=False),
        ),
    ]