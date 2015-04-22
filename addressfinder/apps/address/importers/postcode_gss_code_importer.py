import os
import csv
import time
import subprocess


from dateutil.parser import parse as parsedate

from address.models import PostcodeGssCode


class PostcodeGssCodeImporter(object):
    def import_postcode_gss_codes(self, filename):
        lines = self.lines_in_file(filename)
        start_time = time.time()

        with open(filename, "rb") as csvfile:
            datareader = csv.reader(csvfile)
            count = 0
            for row in datareader:
                print 'importing row ' + str(count) + ' of ' + str(lines - 1)
                self.import_row(row)
                count += 1
                eta_seconds = self.time_remaining(start_time, lines, count)
                print ' - est time remaining = ' + self.hours_minutes_seconds(eta_seconds)

            print 'ALL DONE'

    def time_remaining(self, start_time, lines, count):
        cumulative_time = time.time() - start_time
        time_per_row = cumulative_time / count
        lines_remaining = lines - count
        print "cumulative_time: %is (%s), processed: %i, remaining: %i, time_per_row: %f " %  (cumulative_time, hours_minutes_seconds(cumulative_time), count, lines_remaining, time_per_row)
        return lines_remaining * time_per_row 

    def hours_minutes_seconds(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    def lines_in_file(self, filename):
        output = subprocess.check_output(['wc', '-l', filename], shell=False)
        lines = int( output.split()[0].strip() )
        return lines

    def import_row(self, row):
        postcode = row[0]
        local_authority_gss_code = row[11]
        normalized_postcode = postcode.replace(' ', '').lower()
        mapping = self.find_or_create_lookup( normalized_postcode )
        mapping.local_authority_gss_code = local_authority_gss_code
        mapping.save()

    def find_or_create_lookup(self, postcode_index):
        try:
            a = PostcodeGssCode.objects.get(postcode_index=postcode_index)
        except PostcodeGssCode.DoesNotExist:
            print 'no existing PostcodeGssCode for postcode ' + postcode_index + ' - building...'
            a = PostcodeGssCode(postcode_index=postcode_index)
        return a
