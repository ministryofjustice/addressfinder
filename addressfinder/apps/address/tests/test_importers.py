import os
from datetime import date

from django.test import TestCase
from django.core.management import call_command

from address.models import DeliveryPointAddress, BLPU, Classification, \
    LPI, Organisation, ApplicationCrossReference, Street, StreetDescriptor, \
    SuccessorRecord
from address import constants


class DeliveryPointAddressFormatterTestCase(TestCase):
    def test_full(self):
        call_command(
            'import_addressbase_premium',
            os.path.join(os.path.dirname(__file__), 'data', 'full'),
            **{
                'no_multiprocessing': True,
                'from': 1,
                'to': 999
            }
        )

        # street
        self.assertEqual(Street.objects.count(), 1)
        street = Street.objects.all()[0]
        self.assertEqual(street.usrn, '18300001')
        self.assertEqual(
            street.record_type,
            constants.STREET_RECORD_TYPE_CODE.STREET_DESCRIPTION
        )
        self.assertEqual(street.swa_org_ref_naming, '6805')
        self.assertEqual(
            street.state,
            constants.STREET_STATE_CODE.OPEN
        )
        self.assertEqual(street.state_date, date(year=1990, month=1, day=1))
        self.assertEqual(
            street.street_surface,
            constants.STREET_SURFACE_CODE.METALLED
        )
        self.assertEqual(
            street.street_classification,
            constants.STREET_CLASSIFICATION_CODE.ALL_VEHICLES
        )
        self.assertEqual(street.version, '0')
        self.assertEqual(street.street_start_date, date(year=2003, month=12, day=3))
        self.assertEqual(street.street_end_date, date(year=2003, month=12, day=1))
        self.assertEqual(street.last_update_date, date(year=2011, month=9, day=21))
        self.assertEqual(street.record_entry_date, date(year=2003, month=12, day=3))
        self.assertEqual(street.street_start_coords.x, -4.190881200752782)
        self.assertEqual(street.street_start_coords.y, 53.22478842071331)
        self.assertEqual(street.street_end_coords.x, -4.179644074870196)
        self.assertEqual(street.street_end_coords.y, 53.23154875133635)
        self.assertEqual(street.street_tolerance, 10)

        # street descriptor
        self.assertEqual(StreetDescriptor.objects.count(), 2)
        sd = StreetDescriptor.objects.filter(
            language=constants.LANGUAGE_CODE.ENG
        )[0]
        self.assertEqual(sd.sd_key, '18300001ENG')
        self.assertEqual(sd.usrn, '18300001')
        self.assertEqual(sd.street_description, 'description eng')
        self.assertEqual(sd.locality_name, 'location eng')
        self.assertEqual(sd.town_name, 'town_name eng')
        self.assertEqual(sd.administrative_area, 'administrative area eng')
        self.assertEqual(sd.language, constants.LANGUAGE_CODE.ENG)

        # BLPU
        self.assertEqual(BLPU.objects.count(), 1)
        blpu = BLPU.objects.all()[0]
        self.assertEqual(blpu.uprn, '100020576017')
        self.assertEqual(
            blpu.logical_status,
            constants.LOGICAL_STATUS_CODE.APPROVED
        )
        self.assertEqual(
            blpu.logical_status,
            constants.BLPU_STATE_CODE.UNDER_CONSTRUCTION
        )
        self.assertEqual(blpu.blpu_state_date, date(year=2000, month=11, day=22))
        self.assertEqual(blpu.parent_uprn, '100020576016')
        self.assertEqual(blpu.coords.x, -0.13270949875119267)
        self.assertEqual(blpu.coords.y, 51.31577198495121)

        self.assertEqual(ApplicationCrossReference.objects.count(), 1)
        self.assertEqual(LPI.objects.count(), 1)
        self.assertEqual(DeliveryPointAddress.objects.count(), 1)
        self.assertEqual(Organisation.objects.count(), 1)
        self.assertEqual(Classification.objects.count(), 1)
