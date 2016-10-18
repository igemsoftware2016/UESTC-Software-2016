# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transform', '0003_auto_20161003_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('encode_name', models.CharField(max_length=256)),
                ('encode_token', models.CharField(max_length=256)),
                ('encode_file', models.FileField(upload_to=b'upload/')),
                ('encode_date', models.DateTimeField(auto_now_add=True)),
                ('encode_ip', models.CharField(max_length=256)),
                ('encode_session', models.CharField(max_length=256)),
            ],
        ),
        migrations.DeleteModel(
            name='EncodeFile',
        ),
    ]
