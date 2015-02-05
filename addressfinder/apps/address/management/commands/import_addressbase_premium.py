import time
import os
import csv
from multiprocessing import Pool

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError

from address.models import DeliveryPointAddress, BLPU, Classification, \
    LPI, Organisation, ApplicationCrossReference, Street, StreetDescriptor, \
    SuccessorRecord

from . import import_settings


class BaseImporter(object):
    headers = []
    model = None

    def __init__(self):
        super(BaseImporter, self).__init__()
        self.change_type_idx = self.headers.index('change_type')
        self.updates = []
        self.inserts = []
        self.deletes = []

        self.field_names = []
        self.non_char_field_names = []
        for f in self.model._meta.fields:
            self.field_names.append(f.name)
            if not f.__class__.__name__ == 'CharField':
                self.non_char_field_names.append(f.name)

    def get_ab_primary_key(self, row):
        return row[self.ab_pk_field_index]

    def post_process(self, row, obj_data):
        return obj_data

    def import_row(self, row):
        obj_data = {}
        for i, h in enumerate(self.headers):
            if h not in self.field_names:
                continue
            val = row[i]
            if not val and h in self.non_char_field_names:
                val = None
            obj_data[h] = val
        obj_data = self.post_process(row, obj_data)

        # add to insert, update, delete list
        change_type = row[self.change_type_idx]
        if change_type == 'I':
            self.inserts.append(self.model(**obj_data))
        elif change_type == 'U':
            self.updates.append(obj_data)
        elif change_type == 'D':
            self.deletes.append(obj_data[self.model._meta.pk.name])
        else:
            raise ValidationError(
                u"change type %s not supported" % change_type
            )

    def save(self):
        self.model.objects.bulk_create(self.inserts)
        for obj_data in self.updates:
            self.model.objects.filter(pk=obj_data[self.model._meta.pk.name]).update(**obj_data)
        self.model.objects.filter(pk__in=self.deletes).delete()

        return (len(self.inserts), len(self.updates), len(self.deletes))


class DeliveryPointAddressImporter(BaseImporter):
    headers = import_settings.HEADERS_DELIVERY_POINT_ADDRESS
    model = DeliveryPointAddress

    def __init__(self):
        super(DeliveryPointAddressImporter, self).__init__()
        self.postcode_idx = self.headers.index('postcode')

    def post_process(self, row, obj_data):
        obj_data['postcode_index'] = row[self.postcode_idx].replace(' ', '').lower()
        return obj_data


class BLPUImporter(BaseImporter):
    headers = import_settings.HEADERS_BLPU
    model = BLPU

    def __init__(self):
        super(BLPUImporter, self).__init__()
        self.x_coord_idx = self.headers.index('x_coordinate')
        self.y_coord_idx = self.headers.index('y_coordinate')

    def post_process(self, row, obj_data):
        obj_data['coords'] = Point(
            float(row[self.x_coord_idx]),
            float(row[self.y_coord_idx]),
            srid=27700
        )
        return obj_data


class ClassificationImporter(BaseImporter):
    headers = import_settings.HEADERS_CLASSIFICATION
    model = Classification


class LPIImporter(BaseImporter):
    headers = import_settings.HEADERS_LPI
    model = LPI


class OrganisationImporter(BaseImporter):
    headers = import_settings.HEADERS_ORGANIZATION
    model = Organisation


class ApplicationCrossReferenceImporter(BaseImporter):
    headers = import_settings.HEADERS_APPLICATION_CROSS_REFERENCE
    model = ApplicationCrossReference


class StreetImporter(BaseImporter):
    headers = import_settings.HEADERS_STREET
    model = Street

    def __init__(self):
        super(StreetImporter, self).__init__()
        self.street_start_x_idx = self.headers.index('street_start_x')
        self.street_start_y_idx = self.headers.index('street_start_y')
        self.street_end_x_idx = self.headers.index('street_end_x')
        self.street_end_y_idx = self.headers.index('street_end_y')

    def post_process(self, row, obj_data):
        obj_data['street_start_coords'] = Point(
            float(row[self.street_start_x_idx]),
            float(row[self.street_start_y_idx]),
            srid=27700
        )
        obj_data['street_end_coords'] = Point(
            float(row[self.street_end_x_idx]),
            float(row[self.street_end_y_idx]),
            srid=27700
        )
        return obj_data


class StreetDescriptorImporter(BaseImporter):
    headers = import_settings.HEADERS_STEET_DESCRIPTOR
    model = StreetDescriptor


class SuccessorRecordImporter(BaseImporter):
    headers = import_settings.HEADERS_SUCCESSOR
    model = SuccessorRecord


def get_importers():
    return {
        '11': StreetImporter(),
        '15': StreetDescriptorImporter(),
        '23': ApplicationCrossReferenceImporter(),
        '21': BLPUImporter(),
        '24': LPIImporter(),
        '28': DeliveryPointAddressImporter(),
        '30': SuccessorRecordImporter(),
        '31': OrganisationImporter(),
        '32': ClassificationImporter(),
    }


def import_csv(filename):
    if not os.access(filename, os.R_OK):
        raise CommandError('CSV file could not be read')

    importers = get_importers()
    with open(filename, 'rb') as csvfile:
        for row in csv.reader(csvfile):
            try:
                importers[row[0]].import_row(row)
            except KeyError:
                pass

    tot_inserts = 0
    tot_updates = 0
    tot_deletes = 0
    for importer in importers.values():
        i, u, d = importer.save()
        tot_inserts += i
        tot_updates += u
        tot_deletes += d

    print 'Recap:'
    print 'Inserts: %d' % tot_inserts
    print 'Updates: %d' % tot_updates
    print 'Deletes: %d' % tot_deletes


class Command(BaseCommand):
    args = '<csv_file csv_file...>'

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('You must specify at least one CSV file')

        start = time.time()
        import_csv(args[0])
        end = time.time()
        # p = Pool()
        # p.map(import_csv, args)

        print 'Took: %s secs' % (end - start)
