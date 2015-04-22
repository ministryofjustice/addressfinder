import os
import csv

from rdflib import Graph, URIRef

from address.models import LocalAuthority


class LocalAuthoritiesImporter(object):

    def __init__(self):
        self.graph = None

    def import_local_authorities(self, filename):
        self.graph = self.load_graph(filename)

        print 'Existing LocalAuthority count = ' + str(LocalAuthority.objects.count())
        # all subject/object pairs which are related by a gssCode
        codes = self.graph.triples( (None, URIRef("http://data.ordnancesurvey.co.uk/ontology/admingeo/gssCode"), None) )

        for code_tuple in codes:
            self.import_gss_code( code_tuple )

        print 'New LocalAuthority count = ' + str(LocalAuthority.objects.count())


    def import_gss_code(self, code_tuple):
        code = str(code_tuple[2])
        print 'importing gss_code ' + str(code)
        local_authority = find_or_create_local_authority(code)
        print 'looking up name for ' + str(code_tuple[0])
        name = self.graph.value( subject=code_tuple[0], predicate=URIRef("http://www.w3.org/2000/01/rdf-schema#label" ) )
        print '=> "' + name + '"'
        self.update_local_authority_name_if_needed(local_authority, name)


    def update_local_authority_name_if_needed(self, local_authority, name):
        print 'existing name is "' + local_authority.name + '"'
        if local_authority.name == name:
            print ' - matches, nothing to do'
        else:
            print ' - updating'
            local_authority.name = name
            print local_authority.__dict__
            local_authority.save()
        

    def find_or_create_local_authority(self, gss_code):
        try:
            a = LocalAuthority.objects.get(gss_code=gss_code)
        except LocalAuthority.DoesNotExist:
            print 'no existing local_authority with gss_code ' + gss_code + ' - creating...'
            a = LocalAuthority(gss_code=gss_code)
        return a

    def lines_in_file(self, filename):
        output = subprocess.check_output(['wc', '-l', filename], shell=False)
        lines = int( output.split()[0].strip() )
        return lines

    def load_graph(self, filename):
        self.graph = Graph()
        print 'parsing graph from file ' + filename + ' with ' + self.lines_in_file(filename) + ' lines'
        self.graph.parse(filename, format="nt")
        print ' => ' + str(len(g)) + ' tuples'
        return self.graph