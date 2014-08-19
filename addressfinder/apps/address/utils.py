import re

from titlecase import titlecase


class AddressFormatter(object):
    """
    Heavily inspired by https://github.com/DanMeakin/getputpostcode
    """
    @classmethod
    def format(cls, address):
        addr = u''

        for k in ['department_name', 'organisation_name', 'po_box_number']:
            v = titlecase(getattr(address, k))
            if v:
                addr += u"%s\n" % v

        addr += cls.format_building(address.sub_building_name,
                                    address.building_name,
                                    address.building_number)

        for k in ['dependent_thoroughfare_name', 'thoroughfare_name',
                  'double_dependent_locality', 'dependent_locality',
                  'post_town', 'postcode']:
            if k == 'postcode':
                addr += u"%s\n" % getattr(address, k)
            elif getattr(address, k):
                addr += u"%s\n" % titlecase(getattr(address, k))

        return '\n'.join(a for a in addr.split('\n') if a)

    @classmethod
    def format_building(cls, sub_name, name, number):
        if not any([sub_name, name, number]):
            return ''

        # Define exception to the usual rule requiring a newline for the
        # building name. See p. 27 of PAF Guide for further information.
        building_str = ''
        exception = re.compile(r"^\d.*\d$|^\d.*\d[A-Za-z]$|^\d[A-Za-z]$|^.$")

        for component in [sub_name, name]:
            if component and exception.match(component):
                building_str += component
                if re.match(r"^[A-Za-z]$", component):
                    building_str += u", "
                else:
                    building_str += u" "
            else:
                # Check if final portion of string is numeric/alphanumeric. If
                # so, split and apply exception to that section only.
                parts = titlecase(component).split(' ')
                final = parts.pop()

                if (exception.match(component)
                            and not number
                            and not re.match(r'/^\d*$/', final)
                        ):
                    building_str += u"%s\n%s " % (' '.join(parts), final)
                else:
                    building_str += u"%s\n" % titlecase(component)

        if number:
            building_str += u"%d " % number

        return building_str.lstrip()
