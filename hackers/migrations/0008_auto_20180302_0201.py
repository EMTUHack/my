# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-02 05:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackers', '0007_auto_20180302_0007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='hacker',
            name='second_chance',
        ),
        migrations.AddField(
            model_name='hacker',
            name='admitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='hacker',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='hacker',
            name='incomplete',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='hacker',
            name='unverified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='hacker',
            name='waitlist',
            field=models.BooleanField(default=False),
        ),
    ]
