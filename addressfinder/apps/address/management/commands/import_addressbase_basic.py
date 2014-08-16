import os
import csv
from collections import OrderedDict

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from dateutil.parser import parse as parsedate

from address.models import Address


class Command(BaseCommand):
    args = 'CSV_FILE'

    headers = OrderedDict([
        ("uprn", "char"),
        ("os_address_toid", "char"),
        ("rm_udprn", "char"),
        ("organisation_name", "char"),
        ("department_name", "char"),
        ("po_box_number", "char"),
        ("building_name", "char"),
        ("sub_building_name", "char"),
        ("building_number", "int"),
        ("dependent_thoroughfare_name", "char"),
        ("thoroughfare_name", "char"),
        ("post_town", "char"),
        ("double_dependent_locality", "char"),
        ("dependent_locality", "char"),
        ("postcode", "char"),
        ("postcode_type", "char"),
        ("x_coordinate", "point"),
        ("y_coordinate", "point"),
        ("rpc", "int"),
        ("change_type", "char"),
        ("start_date", "date"),
        ("last_update_date", "date"),
        ("entry_date", "date"),
        ("primary_class", "char"),
        ("process_date", "date"),
    ])

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('You must specify a CSV file')

        filename = args[0]

        if not os.access(filename, os.R_OK):
            raise CommandError('CSV file could not be read')

        uprn_idx = self.headers.keys().index('uprn')
        postcode_idx = self.headers.keys().index('postcode')
        x_coord_idx = self.headers.keys().index('x_coordinate')
        y_coord_idx = self.headers.keys().index('y_coordinate')

        with open(filename, 'rb') as csvfile:
            for row in csv.reader(csvfile):
                print 'Importing UPRN %s' % row[uprn_idx]

                try:
                    a = Address.objects.get(uprn=row[uprn_idx])
                except Address.DoesNotExist:
                    a = Address()

                for i, (k, v) in enumerate(self.headers.iteritems()):
                    if v == 'char':
                        setattr(a, k, row[i])
                    if v == 'int' and row[i] != '':
                        setattr(a, k, int(row[i]))
                    if v == 'date' and row[i] != '':
                        setattr(a, k, parsedate(row[i]))

                a.postcode_index = row[postcode_idx].replace(' ', '').lower()

                a.point = Point(
                    float(row[x_coord_idx]),
                    float(row[y_coord_idx]),
                    srid=27700
                )

                a.save()
