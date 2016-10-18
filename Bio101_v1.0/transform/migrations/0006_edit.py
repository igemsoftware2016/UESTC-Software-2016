# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transform', '0005_auto_20161005_0150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('edit_token1', models.CharField(max_length=256)),
                ('edit_token2', models.CharField(max_length=256)),
            ],
        ),
    ]
