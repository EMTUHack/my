# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-27 03:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackers', '0005_auto_20171025_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='hacker',
            name='second_chance',
            field=models.BooleanField(default=False),
        ),
    ]