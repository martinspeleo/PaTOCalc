# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-31 09:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0005_auto_20160130_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='forminstance',
            name='form_generator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calc.FormGenerator'),
            preserve_default=False,
        ),
    ]
