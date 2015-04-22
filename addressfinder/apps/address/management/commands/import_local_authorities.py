import os
import rdflib

from multiprocessing import Pool

from collections import OrderedDict

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from dateutil.parser import parse as parsedate

from address.importers.local_authorities_importer import LocalAuthoritiesImporter



class Command(BaseCommand):
    args = '<nt_file nt_file...>'

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('You must specify at least one .nt file - you might want to download one from, for example, http://opendatacommunities.org/data/dev-local-authorities/dump')

        p = Pool()
        p.map(import_local_authorities, args)


def import_local_authorities(filename):
    if not os.access(filename, os.R_OK):
        raise CommandError('.nt file ' + filename + ' could not be read')

    importer = LocalAuthoritiesImporter()
    importer.import_local_authorities(filename)
