# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_HOI', '0018_auto_20150901_1130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoria',
            name='accion',
        ),
        migrations.RemoveField(
            model_name='categoria',
            name='fecha_accion',
        ),
        migrations.RemoveField(
            model_name='categoria',
            name='id_usuario_accion',
        ),
        migrations.RemoveField(
            model_name='item',
            name='accion',
        ),
        migrations.RemoveField(
            model_name='item',
            name='fecha_accion',
        ),
        migrations.RemoveField(
            model_name='item',
            name='id_usuario_accion',
        ),
    ]
