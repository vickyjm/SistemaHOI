# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_HOI', '0016_auto_20150901_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='fecha_accion',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 1, 11, 30, 22, 998235)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='fecha_accion',
            field=models.DateTimeField(verbose_name=datetime.datetime(2015, 9, 1, 11, 30, 22, 999148)),
            preserve_default=True,
        ),
    ]
