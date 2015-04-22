# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0004_local_authorities_and_gss_codes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcodegsscode',
            name='local_authority_gss_code',
            field=models.CharField(max_length=9, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='postcodegsscode',
            name='postcode_index',
            field=models.CharField(max_length=7, serialize=False, primary_key=True, db_index=True),
            preserve_default=True,
        ),
    ]
