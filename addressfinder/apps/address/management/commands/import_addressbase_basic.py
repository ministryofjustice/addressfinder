import os
import csv
from decimal import Decimal

from dateutil.parser import parse as parsedate

from django.core.management.base import BaseCommand, CommandError

from address.models import Address


class Command(BaseCommand):
    args = 'CSV_FILE'

    headers = [
        "uprn",
        "os_address_toid",
        "rm_udprn",
        "organisation_name",
        "department_name",
        "po_box_number",
        "building_name",
        "sub_building_name",
        "building_number",
        "dependent_thoroughfare_name",
        "thoroughfare_name",
        "post_town",
        "double_dependent_locality",
        "dependent_locality",
        "postcode",
        "postcode_type",
        "x_coordinate",
        "y_coordinate",
        "rpc",
        "change_type",
        "start_date",
        "last_update_date",
        "entry_date",
        "primary_class",
        "process_date"
    ]

    char_fields = [
        "uprn",
        "os_address_toid",
        "rm_udprn",
        "organisation_name",
        "department_name",
        "po_box_number",
        "building_name",
        "sub_building_name",
        "dependent_thoroughfare_name",
        "thoroughfare_name",
        "post_town",
        "double_dependent_locality",
        "dependent_locality",
        "postcode",
        "postcode_type",
        "change_type",
        "primary_class"
    ]

    integer_fields = [
        "building_number",
        "rpc"
    ]

    decimal_fields = [
        "x_coordinate",
        "y_coordinate"
    ]

    date_fields = [
        "start_date",
        "last_update_date",
        "entry_date",
        "process_date"
    ]

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('You must specify a CSV file')

        filename = args[0]

        if not os.access(filename, os.R_OK):
            raise CommandError('CSV file could not be read')

        with open(filename, 'rb') as csvfile:
            for row in csv.reader(csvfile):
                print 'Importing UPRN %s' % row[self.headers.index('uprn')]

                try:
                    a = Address.objects.get(
                        uprn=row[self.headers.index('uprn')])
                except Address.DoesNotExist:
                    a = Address()

                for f in self.char_fields:
                    setattr(a, f, row[self.headers.index(f)])

                for f in self.integer_fields:
                    if row[self.headers.index(f)] != '':
                        setattr(a, f, int(row[self.headers.index(f)]))

                for f in self.decimal_fields:
                    if row[self.headers.index(f)] != '':
                        setattr(a, f, Decimal(row[self.headers.index(f)]))

                for f in self.date_fields:
                    if row[self.headers.index(f)] != '':
                        setattr(a, f, parsedate(row[self.headers.index(f)]))

                a.postcode_index = row[self.headers.index('postcode')].\
                    replace(' ', '').lower()

                a.save()
