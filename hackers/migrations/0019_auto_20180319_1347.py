# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-19 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackers', '0018_application_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hacker',
            name='azure_pass',
        ),
        migrations.AlterField(
            model_name='hacker',
            name='fb_social_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='hacker',
            name='gh_social_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
