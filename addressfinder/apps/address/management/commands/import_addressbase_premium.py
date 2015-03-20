import time
import os
import csv
from optparse import make_option
from multiprocessing import Pool

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.db import transaction

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

        self._headers_data = [(i, h) for i, h in enumerate(self.headers) if h in self.field_names]

    def post_process(self, row, obj_data):
        return obj_data

    def import_row(self, row):
        obj_data = {}
        for i, h in self._headers_data:
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
            self.updates.append(self.model(**obj_data))
        elif change_type == 'D':
            self.deletes.append(self.model(**obj_data))
        else:
            raise ValidationError(
                u"change type %s not supported" % change_type
            )

    def save(self):
        tot_inserts = len(self.inserts)
        tot_updates = len(self.updates)
        tot_deletes = len(self.deletes)

        # optimization, delete 'updates' and reinsert them
        to_delete = [obj.pk for obj in self.updates + self.deletes]
        self.model.objects.filter(pk__in=to_delete).delete()

        self.inserts += self.updates
        self.model.objects.bulk_create(self.inserts)

        return (tot_inserts, tot_updates, tot_deletes)


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

    def __init__(self):
        super(StreetDescriptorImporter, self).__init__()
        self.usrn_idx = self.headers.index('usrn')
        self.language_idx = self.headers.index('language')

    def post_process(self, row, obj_data):
        obj_data['sd_key'] = '%s%s' % (
            row[self.usrn_idx], row[self.language_idx]
        )
        return obj_data


class SuccessorRecordImporter(BaseImporter):
    headers = import_settings.HEADERS_SUCCESSOR
    model = SuccessorRecord


def get_importers():
    return {
        '11': StreetImporter(),
        '15': StreetDescriptorImporter(),
        '21': BLPUImporter(),
        '23': ApplicationCrossReferenceImporter(),
        '24': LPIImporter(),
        '28': DeliveryPointAddressImporter(),
        '30': SuccessorRecordImporter(),
        '31': OrganisationImporter(),
        '32': ClassificationImporter(),
    }


def import_csv(filepath):
    start = time.time()

    # import
    importers = get_importers()
    with open(filepath, 'rb') as csvfile:
        for row in csv.reader(csvfile):
            try:
                importers[row[0]].import_row(row)
            except KeyError:
                pass

    filename = os.path.basename(filepath)
    try:
        with transaction.atomic():
            # save
            tot_inserts = 0
            tot_updates = 0
            tot_deletes = 0
            for importer in importers.values():
                i, u, d = importer.save()
                tot_inserts += i
                tot_updates += u
                tot_deletes += d

            # recap
            end = time.time()
            print '\nFinished processing %s, took: %s secs' % (
                filename, end - start
            )
            print 'Recap:'
            print 'Inserts: %d' % tot_inserts
            print 'Updates: %d' % tot_updates
            print 'Deletes: %d' % tot_deletes
    except Exception:
        print "File %s not imported because of exception" % filename

class Command(BaseCommand):
    args = '<base-dir>'
    option_list = BaseCommand.option_list + (
        make_option(
            '--from',
            action='store',
            dest='from',
            type="int",
            default=1,
            help='First file number to process (default 1)'
        ),
        make_option(
            '--to',
            action='store',
            dest='to',
            type="int",
            default=999,
            help='Last file number to process (default to last in folder)'
        ),
        make_option(
            '--no-multiprocessing',
            action='store_true',
            dest='no_multiprocessing',
            default=False,
            help='If True, it will import files one after another'
        )
    )

    def build_filepaths(self):
        filepaths = []

        index = self.from_filenum
        path_template = self.get_path_template_for_filenum(self.from_filenum)
        while index <= self.to_filenum:
            filename = path_template % ("%03d" % index, )
            if os.access(filename, os.R_OK):
                filepaths.append(filename)
                index += 1
            else:
                # see if it's in another folder
                try:
                    path_template = self.get_path_template_for_filenum(index)
                except CommandError:
                    self.to_filenum = index - 1
                    break
        return filepaths

    def get_path_template_for_filenum(self, filenum):
        looking_for = "%03d.csv" % filenum
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith(looking_for):
                    return os.path.join(
                        root, file.replace(looking_for, '%s.csv')
                    )
        raise CommandError(
            'File ending in %s not found in %s' % (
                looking_for, self.base_dir
            )
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('You must specify only the base dir as arg')
        self.base_dir = args[0]

        self.from_filenum = options['from']
        self.to_filenum = options['to']

        filepaths = self.build_filepaths()

        if options['no_multiprocessing']:
            for filepath in filepaths:
                import_csv(filepath)
        else:
            p = Pool(maxtasksperchild=4)
            p.map(import_csv, filepaths)
