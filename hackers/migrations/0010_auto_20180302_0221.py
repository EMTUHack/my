# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-02 05:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackers', '0009_hacker_declined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hacker',
            name='token',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
