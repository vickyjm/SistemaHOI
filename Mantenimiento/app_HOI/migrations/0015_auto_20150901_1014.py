# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_HOI', '0014_auto_20150901_1014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='id_usuario_accion',
        ),
        migrations.AlterField(
            model_name='item',
            name='fecha_accion',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 1, 10, 14, 34, 536057)),
            preserve_default=True,
        ),
    ]
