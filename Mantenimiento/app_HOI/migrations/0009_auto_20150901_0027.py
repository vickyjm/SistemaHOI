# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_HOI', '0008_auto_20150831_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='accion',
            field=models.PositiveIntegerField(default=0, choices=[(0, 'Crea'), (1, 'Modifica'), (2, 'Ingresa')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='fecha_accion',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 1, 0, 27, 36, 400213)),
            preserve_default=True,
        ),
    ]
