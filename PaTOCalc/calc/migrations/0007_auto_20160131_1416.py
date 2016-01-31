# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0006_forminstance_form_generator'),
    ]

    operations = [
        migrations.AddField(
            model_name='forminstance',
            name='patient_data',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='forminstance',
            name='form_generator',
            field=models.ForeignKey(blank=True, to='calc.FormGenerator', null=True),
        ),
    ]
