# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0003_populate_postcode_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalAuthority',
            fields=[
                ('gss_code', models.CharField(max_length=9, serialize=False, primary_key=True, db_index=True)),
                ('name', models.CharField(max_length=128, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostcodeGssCode',
            fields=[
                ('postcode_index', models.CharField(max_length=7, db_index=True)),
                ('local_authority_gss_code', models.CharField(max_length=9, serialize=False, primary_key=True, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='address',
            name='postcode_area',
            field=models.CharField(default=b'', max_length=4, db_index=True, blank=True),
            preserve_default=True,
        ),
    ]
