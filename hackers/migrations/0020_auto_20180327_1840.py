# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-03-27 21:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackers', '0019_auto_20180319_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='hacker',
            name='full_name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='application',
            name='essay',
            field=models.TextField(null=True),
        ),
    ]
