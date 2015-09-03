# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_HOI', '0004_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='accion',
            field=models.PositiveIntegerField(default=0, choices=[(0, 'Crea'), (1, 'Modifica')]),
            preserve_default=True,
        ),
    ]
