import os
import csv
from multiprocessing import Pool

from collections import OrderedDict

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from django.db.utils import DataError

from dateutil.parser import parse as parsedate

from address.models import Address


class Command(BaseCommand):
    args = '<csv_file csv_file...>'

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('You must specify at least one CSV file')

        p = Pool()
        p.map(import_csv, args)


def import_csv(filename):
    headers = OrderedDict([
        ('uprn', 'int'),
        ('rm_udprn', 'int'),
        ('change_type', 'char'),
        ('state', 'int'),
        ('state_date', 'date'),
        ('classification', 'char'),
        ('parent_uprn', 'int'),
        ('x_coordinate', 'point'),
        ('y_coordinate', 'point'),
        ('rpc', 'int'),
        ('local_custodian_code', 'char'),
        ('start_date', 'date'),
        ('end_date', 'date'),
        ('last_update_date', 'date'),
        ('entry_date', 'date'),
        ('organisation_name', 'char'),
        ('organisation', 'char'),
        ('department_name', 'char'),
        ('scottish_department_name', 'char'),
        ('building_name', 'char'),
        ('sub_building_name', 'char'),
        ('sao_start_number', 'int'),
        ('sao_start_suffix', 'char'),
        ('sao_end_number', 'int'),
        ('sao_end_suffix', 'char'),
        ('sao_text', 'char'),
        ('alt_language_sao_text', 'char'),
        ('pao_start_number', 'int'),
        ('pao_start_suffix', 'char'),
        ('pao_end_number', 'int'),
        ('pao_end_suffix', 'char'),
        ('pao_text', 'char'),
        ('alt_language_pao_text', 'char'),
        ('usrn', 'int'),
        ('usrn_match_indicator', 'char'),
        ('area_name', 'char'),
        ('level', 'char'),
        ('official_flag', 'yesno'),
        ('os_address_toid', 'char'),
        ('os_address_toid_version', 'int'),
        ('os_roadlink_toid', 'char'),
        ('os_roadlink_toid_version', 'int'),
        ('os_topo_toid', 'char'),
        ('os_topo_toid_version', 'int'),
        ('voa_ct_record', 'int'),
        ('voa_ndr_record', 'int'),
        ('street_description', 'char'),
        ('alt_language_street_description', 'char'),
        ('dependent_thoroughfare_name', 'char'),
        ('thoroughfare_name', 'char'),
        ('welsh_dependent_thoroughfare_name', 'char'),
        ('welsh_thoroughfare_name', 'char'),
        ('double_dependent_locality', 'char'),
        ('dependent_locality', 'char'),
        ('locality_name', 'char'),
        ('welsh_double_dependent_locality', 'char'),
        ('welsh_dependent_locality', 'char'),
        ('town_name', 'char'),
        ('administrative_area', 'char'),
        ('post_town', 'char'),
        ('postcode', 'char'),
        ('postcode_locator', 'char'),
        ('postcode_type', 'char'),
        ('postal_address', 'char'),
        ('po_box_number', 'char'),
        ('ward_code', 'char'),
        ('parish_code', 'char'),
        ('process_date', 'date'),
        ('multi_occ_count', 'int'),
        ('voa_ndr_p_desc_code', 'char'),
        ('voa_ndr_scat_code', 'char'),
        ('alt_language', 'char'),
    ])

    if not os.access(filename, os.R_OK):
        raise CommandError('CSV file could not be read')

    uprn_idx = headers.keys().index('uprn')
    postcode_idx = headers.keys().index('postcode')
    x_coord_idx = headers.keys().index('x_coordinate')
    y_coord_idx = headers.keys().index('y_coordinate')

    with open(filename, 'rb') as csvfile:
        for row in csv.reader(csvfile):
            print 'Importing UPRN %s' % row[uprn_idx]

            try:
                a = Address.objects.get(uprn=row[uprn_idx])
            except Address.DoesNotExist:
                a = Address()

            for i, (k, v) in enumerate(headers.iteritems()):
                if v == 'char':
                    setattr(a, k, row[i])
                if v == 'int' and row[i] != '':
                    setattr(a, k, int(row[i]))
                if v == 'date' and row[i] != '':
                    setattr(a, k, parsedate(row[i]))
                if v == 'yesno' and row[i] != '':
                    setattr(a, k, True if row[i] == 'Y' else False)

            a.postcode_index = row[postcode_idx].replace(' ', '').lower()

            a.point = Point(
                float(row[x_coord_idx]),
                float(row[y_coord_idx]),
                srid=27700
            )

            a.save()
