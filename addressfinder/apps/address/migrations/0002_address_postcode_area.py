# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='postcode_area',
            field=models.CharField(max_length=4, db_index=True, null=True),
            preserve_default=True,
        ),
    ]
