# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_address_postcode_area'),
    ]

    operations = [
      migrations.RunSQL("UPDATE address_address SET postcode_area = split_part(postcode, ' ', 1);")
    ]
