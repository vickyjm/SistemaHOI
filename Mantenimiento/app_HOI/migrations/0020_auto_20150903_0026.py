# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_HOI', '0019_auto_20150901_1233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='prioridad',
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='estado',
            field=models.CharField(max_length=1, default='E', choices=[('A', 'Aprobado'), ('R', 'Rechazado'), ('E', 'Esperando respuesta')]),
            preserve_default=True,
        ),
    ]
