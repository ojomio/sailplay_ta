# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MessageLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('sms_id', models.IntegerField(blank=True, null=True)),
                ('via_gate', models.CharField(max_length=40)),
                ('sender', models.CharField(max_length=50)),
                ('recepient', models.CharField(max_length=50)),
                ('time', models.DateTimeField(auto_now=True)),
                ('sent_ok', models.BooleanField()),
                ('error_description', models.TextField(max_length=1500, blank=True, null=True)),
            ],
        ),
    ]
