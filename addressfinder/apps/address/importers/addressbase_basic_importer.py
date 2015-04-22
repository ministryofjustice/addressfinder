import os
import csv

from collections import OrderedDict
from django.contrib.gis.geos import Point
from dateutil.parser import parse as parsedate

from address.models import Address


class AddressBaseBasicImporter(object):

    def __init__(self):
        self.headers = self.csv_headers()
        self.indices = self.column_indices()

    def import_csv(self, filename):
        with open(filename, 'rb') as csvfile:
            for row in csv.reader(csvfile):
                print 'Importing UPRN %s' % row[self.indices['uprn']]
                self.import_row(row)

        print "ALL DONE"

    def import_row(self, row):
        try:
            a = Address.objects.get(uprn=row[self.indices['uprn']])
        except Address.DoesNotExist:
            a = Address()

        for i, (k, v) in enumerate(self.headers.iteritems()):
            if v == 'char':
                setattr(a, k, row[i])
            if v == 'int' and row[i] != '':
                setattr(a, k, int(row[i]))
            if v == 'date' and row[i] != '':
                setattr(a, k, parsedate(row[i]))

        a.postcode_index = row[self.indices['postcode']].replace(' ', '').lower()

        a.point = Point(
            float(row[self.indices['x_coord']]),
            float(row[self.indices['y_coord']]),
            srid=27700
        )

        a.save()

    def column_indices(self):
        return {
            'uprn': self.headers.keys().index('uprn'),
            'postcode': self.headers.keys().index('postcode'),
            'x_coord': self.headers.keys().index('x_coordinate'),
            'y_coord': self.headers.keys().index('y_coordinate')
        }

    def csv_headers(self):
        return OrderedDict([
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