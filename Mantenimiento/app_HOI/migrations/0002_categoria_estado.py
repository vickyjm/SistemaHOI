# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_HOI', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='estado',
            field=models.PositiveIntegerField(default=1, choices=[(0, 'Inactiva'), (1, 'Activa')]),
            preserve_default=True,
        ),
    ]
