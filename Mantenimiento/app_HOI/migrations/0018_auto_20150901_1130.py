# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_HOI', '0017_auto_20150901_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='fecha_accion',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 1, 11, 30, 33, 685227)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='fecha_accion',
            field=models.DateTimeField(verbose_name=datetime.datetime(2015, 9, 1, 11, 30, 33, 686136)),
            preserve_default=True,
        ),
    ]
