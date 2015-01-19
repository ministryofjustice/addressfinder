from multiprocessing import Pool

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.gdal import DataSource

from areas.models import Area


class Command(BaseCommand):
    """
    Imports police service areas from KML files as provided by 
    http://data.police.uk
    """
    args = '<xml_file kml_file...>'

    def handle(self, *args, **kwargs):
        if len(args) == 0:
            raise CommandError('You must specify at least one KML file')

        p = Pool()
        p.map(import_kml, args)


def import_kml(filename):
    ds = DataSource(filename)
    name = filename.split('/')[-1].split('.')[0].replace('-', ' ').title()

    try:
        area = Area.objects.get(name=name, area_type='POL')
    except Area.DoesNotExist:
        area = Area(name=name, area_type='POL')

    # KML includes unneeded Z dimension
    geom = ds[0][0].geom
    geom.coord_dim = 2  # remove 3rd dimension

    area.geom = geom.geos
    area.save()
