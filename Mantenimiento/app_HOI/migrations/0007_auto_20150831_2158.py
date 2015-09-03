# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app_HOI', '0006_item_fecha_accion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='fecha_accion',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 1, 2, 28, 50, 19771, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
