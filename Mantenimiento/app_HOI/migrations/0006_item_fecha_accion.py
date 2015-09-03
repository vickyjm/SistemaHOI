# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_HOI', '0005_item_accion'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='fecha_accion',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 21, 57, 57, 621318)),
            preserve_default=True,
        ),
    ]
