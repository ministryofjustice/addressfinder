# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('uprn', models.CharField(max_length=12, serialize=False, primary_key=True)),
                ('os_address_toid', models.CharField(default=b'', max_length=20, blank=True)),
                ('rm_udprn', models.CharField(max_length=8)),
                ('organisation_name', models.CharField(default=b'', max_length=60, blank=True)),
                ('department_name', models.CharField(default=b'', max_length=60, blank=True)),
                ('po_box_number', models.CharField(default=b'', max_length=6, blank=True)),
                ('building_name', models.CharField(default=b'', max_length=50, blank=True)),
                ('sub_building_name', models.CharField(default=b'', max_length=30, blank=True)),
                ('building_number', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('dependent_thoroughfare_name', models.CharField(default=b'', max_length=80, blank=True)),
                ('thoroughfare_name', models.CharField(default=b'', max_length=80, blank=True)),
                ('post_town', models.CharField(default=b'', max_length=30, blank=True)),
                ('double_dependent_locality', models.CharField(default=b'', max_length=35, blank=True)),
                ('dependent_locality', models.CharField(default=b'', max_length=35, blank=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('postcode', models.CharField(max_length=8)),
                ('postcode_index', models.CharField(max_length=7, db_index=True)),
                ('postcode_type', models.CharField(max_length=1)),
                ('rpc', models.PositiveSmallIntegerField()),
                ('change_type', models.CharField(max_length=1)),
                ('start_date', models.DateField()),
                ('last_update_date', models.DateField()),
                ('entry_date', models.DateField()),
                ('primary_class', models.CharField(max_length=1)),
                ('process_date', models.DateField()),
            ],
            options={
                'ordering': ['building_number', 'building_name', 'sub_building_name'],
                'verbose_name_plural': 'addresses',
            },
            bases=(models.Model,),
        ),
    ]
