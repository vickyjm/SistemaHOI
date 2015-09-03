# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_HOI', '0007_auto_20150831_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='fecha_accion',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 22, 0, 21, 712187)),
            preserve_default=True,
        ),
    ]
