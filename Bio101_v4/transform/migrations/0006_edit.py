# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transform', '0005_auto_20161005_0150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('edit_fragment', models.CharField(max_length=145)),
                ('edit_token', models.CharField(max_length=256)),
            ],
        ),
    ]
