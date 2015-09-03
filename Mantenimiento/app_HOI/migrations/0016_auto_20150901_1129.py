# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_HOI', '0015_auto_20150901_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='accion',
            field=models.PositiveIntegerField(default=0, choices=[(0, 'Creada'), (1, 'Modificada')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categoria',
            name='fecha_accion',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 1, 11, 29, 57, 626153)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categoria',
            name='id_usuario_accion',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='id_usuario_accion',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='accion',
            field=models.PositiveIntegerField(default=0, choices=[(0, 'Creado'), (1, 'Modificado'), (2, 'Ingresado')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='fecha_accion',
            field=models.DateTimeField(verbose_name=datetime.datetime(2015, 9, 1, 11, 29, 57, 627955)),
            preserve_default=True,
        ),
    ]
