import os

from multiprocessing import Pool

from collections import OrderedDict

from django.core.management.base import BaseCommand, CommandError

from address.importers.postcode_gss_code_importer import PostcodeGssCodeImporter

class Command(BaseCommand):
    args = '<csv_file csv_file...>'

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('You must specify at least one CSV file')

        p = Pool()
        p.map(import_csv, args)


def import_csv(filename):
    if not os.access(filename, os.R_OK):
        raise CommandError('CSV file could not be read')

    importer = PostcodeGssCodeImporter()
    importer.import_postcode_gss_codes(filename)


    