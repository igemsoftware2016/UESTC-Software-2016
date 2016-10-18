# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transform', '0004_auto_20161003_2208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Decode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('decode_token', models.CharField(max_length=256)),
                ('decode_file', models.FileField(upload_to=b'upload')),
            ],
        ),
        migrations.RemoveField(
            model_name='encode',
            name='encode_date',
        ),
        migrations.RemoveField(
            model_name='encode',
            name='encode_ip',
        ),
        migrations.RemoveField(
            model_name='encode',
            name='encode_name',
        ),
        migrations.RemoveField(
            model_name='encode',
            name='encode_session',
        ),
        migrations.AlterField(
            model_name='encode',
            name='encode_file',
            field=models.FileField(upload_to=b'upload'),
        ),
    ]
