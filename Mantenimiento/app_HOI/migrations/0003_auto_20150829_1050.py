# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_HOI', '0002_categoria_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='estado',
            field=models.PositiveIntegerField(default=1, choices=[(0, 'Inactivo'), (1, 'Activo')]),
            preserve_default=True,
        ),
    ]
