# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_HOI', '0010_auto_20150901_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='id_usuario_accion',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='fecha_accion',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 1, 9, 57, 58, 602766)),
            preserve_default=True,
        ),
    ]
