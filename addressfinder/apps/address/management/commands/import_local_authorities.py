import os
import rdflib

from multiprocessing import Pool

from collections import OrderedDict

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from dateutil.parser import parse as parsedate

from rdflib import Graph, URIRef

from address.models import LocalAuthority



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

    g = load_graph(filename)

    print 'Existing LocalAuthority count = ' + str(LocalAuthority.objects.count())
    # all subject/object pairs which are related by a gssCode
    codes = g.triples( (None, URIRef("http://data.ordnancesurvey.co.uk/ontology/admingeo/gssCode"), None) )

    for code_tuple in codes:
        import_gss_code( code_tuple, g)

    print 'New LocalAuthority count = ' + str(LocalAuthority.objects.count())


def import_gss_code(code_tuple, graph):
    code = str(code_tuple[2])
    print 'importing gss_code ' + str(code)
    local_authority = find_or_create_local_authority(code)
    print 'looking up name for ' + str(code_tuple[0])
    name = graph.value( subject=code_tuple[0], predicate=URIRef("http://www.w3.org/2000/01/rdf-schema#label" ) )
    print '=> "' + name + '"'
    update_local_authority_name_if_needed(local_authority, name)


def update_local_authority_name_if_needed(local_authority, name):
    print 'existing name is "' + local_authority.name + '"'
    if local_authority.name == name:
        print ' - matches, nothing to do'
    else:
        print ' - updating'
        local_authority.name = name
        print local_authority.__dict__
        local_authority.save()
    

def find_or_create_local_authority(gss_code):
    try:
        a = LocalAuthority.objects.get(gss_code=gss_code)
    except LocalAuthority.DoesNotExist:
        print 'no existing local_authority with gss_code ' + gss_code + ' - creating...'
        a = LocalAuthority(gss_code=gss_code)
    return a

def load_graph(filename):
    g = Graph()
    print 'parsing graph from file ' + filename
    g.parse(filename, format="nt")
    print ' => ' + str(len(g)) + ' tuples'
    return g