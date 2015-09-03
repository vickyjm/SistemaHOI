# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app_HOI', '0011_auto_20150901_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='fecha_accion',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 1, 10, 12, 21, 194999)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='id_usuario_accion',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
