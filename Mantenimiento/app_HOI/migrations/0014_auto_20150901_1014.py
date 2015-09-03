# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_HOI', '0013_auto_20150901_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='fecha_accion',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 1, 10, 14, 20, 954888)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='id_usuario_accion',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
