# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-04 05:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_event_place'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='ends',
        ),
    ]
