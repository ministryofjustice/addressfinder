# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationCrossReference',
            fields=[
                ('xref_key', models.CharField(max_length=14, serialize=False, primary_key=True)),
                ('cross_reference', models.CharField(max_length=50)),
                ('version', models.CharField(max_length=3, blank=True)),
                ('source', models.CharField(max_length=6)),
                ('uprn', models.CharField(max_length=12)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('last_update_date', models.DateField()),
                ('entry_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BLPU',
            fields=[
                ('uprn', models.CharField(max_length=12, serialize=False, primary_key=True)),
                ('logical_status', models.PositiveSmallIntegerField(choices=[(1, b'Approved'), (3, b'Alternative'), (6, b'Provisional'), (8, b'Historical')])),
                ('blpu_state', models.PositiveSmallIntegerField(blank=True, null=True, choices=[(1, b'Under construction'), (2, b'In use'), (3, b'Unoccupied'), (4, b'No longer existing'), (6, b'Planning permission granted')])),
                ('blpu_state_date', models.DateField(null=True, blank=True)),
                ('parent_uprn', models.CharField(max_length=12, blank=True)),
                ('coords', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('rpc', models.PositiveSmallIntegerField(choices=[(1, b'Visual centre'), (2, b'General internal point'), (3, b'SW corner of referenced 100 m grid'), (4, b'Start of referenced street'), (5, b'General point based on postcode unit'), (9, b'Centre of a contributing authority area')])),
                ('local_custodian_code', models.PositiveSmallIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('last_update_date', models.DateField()),
                ('entry_date', models.DateField()),
                ('postal_address', models.CharField(max_length=1, choices=[(b'S', b'Single address'), (b'N', b'Non postal address'), (b'C', b'Child address'), (b'M', b'Parent address')])),
                ('postcode_locator', models.CharField(max_length=8)),
                ('multi_occ_count', models.PositiveSmallIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('class_key', models.CharField(max_length=14, serialize=False, primary_key=True)),
                ('uprn', models.CharField(max_length=12)),
                ('classification_code', models.CharField(max_length=6)),
                ('class_scheme', models.CharField(max_length=60)),
                ('scheme_version', models.CharField(max_length=5)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('last_update_date', models.DateField()),
                ('entry_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeliveryPointAddress',
            fields=[
                ('rm_udprn', models.CharField(max_length=8, serialize=False, primary_key=True)),
                ('uprn', models.CharField(max_length=12)),
                ('parent_addressable_uprn', models.CharField(max_length=12, blank=True)),
                ('organisation_name', models.CharField(max_length=60, blank=True)),
                ('department_name', models.CharField(max_length=60, blank=True)),
                ('sub_building_name', models.CharField(max_length=30, blank=True)),
                ('building_name', models.CharField(max_length=50, blank=True)),
                ('building_number', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('dependent_thoroughfare_name', models.CharField(max_length=80, blank=True)),
                ('thoroughfare_name', models.CharField(max_length=80, blank=True)),
                ('double_dependent_locality', models.CharField(max_length=35, blank=True)),
                ('dependent_locality', models.CharField(max_length=35, blank=True)),
                ('post_town', models.CharField(max_length=30)),
                ('postcode_index', models.CharField(max_length=7, db_index=True)),
                ('postcode', models.CharField(max_length=8)),
                ('postcode_type', models.CharField(max_length=1, choices=[(b'S', b'Small user'), (b'L', b'Large user')])),
                ('welsh_dependent_thoroughfare_name', models.CharField(max_length=80, blank=True)),
                ('welsh_thoroughfare_name', models.CharField(max_length=80, blank=True)),
                ('welsh_double_dependent_locality', models.CharField(max_length=35, blank=True)),
                ('welsh_dependent_locality', models.CharField(max_length=35, blank=True)),
                ('welsh_post_town', models.CharField(max_length=30, blank=True)),
                ('po_box_number', models.CharField(max_length=6, blank=True)),
                ('process_date', models.DateField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('last_update_date', models.DateField()),
                ('entry_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LPI',
            fields=[
                ('lpi_key', models.CharField(max_length=14, serialize=False, primary_key=True)),
                ('uprn', models.CharField(max_length=12)),
                ('language', models.CharField(max_length=3, choices=[(b'ENG', b'English'), (b'CYM', b'Welsh'), (b'GAE', b'Gaelic (Scottish)'), (b'BIL', b'Bilingual (metadata record identifier only)')])),
                ('logical_status', models.PositiveSmallIntegerField(choices=[(1, b'Approved'), (3, b'Alternative'), (6, b'Provisional'), (8, b'Historical')])),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('last_update_date', models.DateField()),
                ('entry_date', models.DateField()),
                ('sao_start_number', models.CharField(max_length=4, blank=True)),
                ('sao_start_suffix', models.CharField(max_length=2, blank=True)),
                ('sao_end_number', models.CharField(max_length=4, blank=True)),
                ('sao_end_suffix', models.CharField(max_length=2, blank=True)),
                ('sao_text', models.CharField(max_length=90, blank=True)),
                ('pao_start_number', models.CharField(max_length=4, blank=True)),
                ('pao_start_suffix', models.CharField(max_length=2, blank=True)),
                ('pao_end_number', models.CharField(max_length=4, blank=True)),
                ('pao_end_suffix', models.CharField(max_length=2, blank=True)),
                ('pao_text', models.CharField(max_length=90, blank=True)),
                ('usrn', models.CharField(max_length=8)),
                ('usrn_match_indicator', models.CharField(max_length=1, choices=[(b'1', b'Matched manually'), (b'2', b'Matched spatially')])),
                ('area_name', models.CharField(max_length=35, blank=True)),
                ('level', models.CharField(max_length=30, blank=True)),
                ('official_flag', models.CharField(blank=True, max_length=1, choices=[(b'Y', b'Yes'), (b'N', b'No')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('org_key', models.CharField(max_length=14, serialize=False, primary_key=True)),
                ('organisation', models.CharField(max_length=100)),
                ('legal_name', models.CharField(max_length=60, blank=True)),
                ('uprn', models.CharField(max_length=12)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('last_update_date', models.DateField()),
                ('entry_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('usrn', models.CharField(max_length=12, serialize=False, primary_key=True)),
                ('record_type', models.PositiveSmallIntegerField(choices=[(1, b'Official designated street name'), (2, b'Street description'), (3, b'Numbered street'), (4, b'Unofficial street description'), (9, b'Description used for LLPG access')])),
                ('swa_org_ref_naming', models.CharField(max_length=4)),
                ('state', models.PositiveSmallIntegerField(blank=True, null=True, choices=[(1, b'Under construction'), (2, b'Open'), (4, b'Permanently closed')])),
                ('state_date', models.DateField(null=True, blank=True)),
                ('street_surface', models.PositiveSmallIntegerField(blank=True, null=True, choices=[(1, b'Metalled'), (2, b'UnMetalled'), (3, b'Mixed')])),
                ('street_classification', models.PositiveSmallIntegerField(blank=True, null=True, choices=[(4, b'Pedestrian way or footpath'), (6, b'Cycle track or cycleway'), (8, b'All vehicles'), (9, b'Restricted byway'), (10, b'Bridleway')])),
                ('version', models.CharField(max_length=3)),
                ('street_start_date', models.DateField()),
                ('street_end_date', models.DateField(null=True, blank=True)),
                ('last_update_date', models.DateField()),
                ('record_entry_date', models.DateField()),
                ('street_start_coords', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('street_end_coords', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('street_tolerance', models.PositiveSmallIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StreetDescriptor',
            fields=[
                ('sd_key', models.CharField(max_length=15, serialize=False, primary_key=True)),
                ('usrn', models.CharField(max_length=12)),
                ('street_description', models.CharField(max_length=100)),
                ('locality_name', models.CharField(max_length=35, blank=True)),
                ('town_name', models.CharField(max_length=30, blank=True)),
                ('administrative_area', models.CharField(max_length=30)),
                ('language', models.CharField(max_length=3, choices=[(b'ENG', b'English'), (b'CYM', b'Welsh'), (b'GAE', b'Gaelic (Scottish)'), (b'BIL', b'Bilingual (metadata record identifier only)')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SuccessorRecord',
            fields=[
                ('succ_key', models.CharField(max_length=14, serialize=False, primary_key=True)),
                ('uprn', models.CharField(max_length=12)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('last_update_date', models.DateField()),
                ('entry_date', models.DateField()),
                ('successor', models.CharField(max_length=12)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='streetdescriptor',
            unique_together=set([('usrn', 'language')]),
        ),
    ]
