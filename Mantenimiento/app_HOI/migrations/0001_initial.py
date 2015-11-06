# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aprueba',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(unique=True, max_length=100)),
                ('estado', models.PositiveIntegerField(choices=[(0, 'Inactivo'), (1, 'Activo')], default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Crea',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=500)),
                ('estado', models.PositiveIntegerField(choices=[(0, 'Inactivo'), (1, 'Activo')], default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ingresa',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('cantidad', models.PositiveIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cantidad', models.PositiveIntegerField()),
                ('minimo', models.PositiveIntegerField()),
                ('estado', models.PositiveIntegerField(choices=[(0, 'Inactivo'), (1, 'Activo')], default=1)),
                ('id_categoria', models.ForeignKey(to='app_HOI.Categoria')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('cantidad', models.PositiveIntegerField()),
                ('estado', models.CharField(choices=[('A', 'Aprobado'), ('R', 'Rechazado'), ('E', 'Esperando respuesta')], default='E', max_length=1)),
                ('dpto', models.ForeignKey(to='app_HOI.Departamento')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ingresa',
            name='id_item',
            field=models.ForeignKey(to='app_HOI.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ingresa',
            name='id_usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crea',
            name='id_item',
            field=models.ForeignKey(to='app_HOI.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crea',
            name='id_solicitud',
            field=models.ForeignKey(to='app_HOI.Solicitud'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crea',
            name='id_usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aprueba',
            name='id_solicitud',
            field=models.ForeignKey(to='app_HOI.Solicitud'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aprueba',
            name='id_usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
