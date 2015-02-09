import os
from datetime import date

from django.test import TestCase
from django.core.management import call_command
from django.contrib.gis.geos import Point

from address.models import DeliveryPointAddress, BLPU, Classification, \
    LPI, Organisation, ApplicationCrossReference, Street, StreetDescriptor, \
    SuccessorRecord
from address import constants


class DeliveryPointAddressFormatterTestCase(TestCase):
    def assertEqualStreet(self, s1, s2):
        self.assertEqual(s1.usrn, s2.usrn)
        self.assertEqual(s1.record_type, s2.record_type)
        self.assertEqual(s1.swa_org_ref_naming, s2.swa_org_ref_naming)
        self.assertEqual(s1.state, s2.state)
        self.assertEqual(s1.state_date, s2.state_date)
        self.assertEqual(s1.street_surface, s2.street_surface)
        self.assertEqual(s1.street_classification, s2.street_classification)
        self.assertEqual(s1.version, s2.version)
        self.assertEqual(s1.street_start_date, s2.street_start_date)
        self.assertEqual(s1.street_end_date, s2.street_end_date)
        self.assertEqual(s1.last_update_date, s2.last_update_date)
        self.assertEqual(s1.record_entry_date, s2.record_entry_date)
        s1.street_start_coords.transform(27700)
        s1.street_end_coords.transform(27700)
        self.assertAlmostEqual(s1.street_start_coords.x, s2.street_start_coords.x, places=1)
        self.assertAlmostEqual(s1.street_start_coords.y, s2.street_start_coords.y, places=1)
        self.assertAlmostEqual(s1.street_end_coords.x, s2.street_end_coords.x, places=1)
        self.assertAlmostEqual(s1.street_end_coords.y, s2.street_end_coords.y, places=1)
        self.assertEqual(s1.street_tolerance, s2.street_tolerance)

    def assertEqualStreetDescriptor(self, s1, s2):
        self.assertEqual(s1.sd_key, s2.sd_key)
        self.assertEqual(s1.usrn, s2.usrn)
        self.assertEqual(s1.street_description, s2.street_description)
        self.assertEqual(s1.locality_name, s2.locality_name)
        self.assertEqual(s1.town_name, s2.town_name)
        self.assertEqual(s1.administrative_area, s2.administrative_area)
        self.assertEqual(s1.language, s2.language)

    def assertEqualBLPU(self, b1, b2):
        self.assertEqual(b1.uprn, b2.uprn)
        self.assertEqual(b1.logical_status, b2.logical_status)
        self.assertEqual(b1.logical_status, b2.logical_status)
        self.assertEqual(b1.blpu_state_date, b2.blpu_state_date)
        self.assertEqual(b1.parent_uprn, b2.parent_uprn)
        b1.coords.transform(27700)
        self.assertAlmostEqual(b1.coords.x, b2.coords.x, places=1)
        self.assertAlmostEqual(b1.coords.y, b2.coords.y, places=1)
        self.assertEqual(b1.rpc, b2.rpc)
        self.assertEqual(b1.local_custodian_code, b2.local_custodian_code)
        self.assertEqual(b1.start_date, b2.start_date)
        self.assertEqual(b1.end_date, b2.end_date)
        self.assertEqual(b1.last_update_date, b2.last_update_date)
        self.assertEqual(b1.entry_date, b2.entry_date)
        self.assertEqual(b1.postal_address, b2.postal_address)
        self.assertEqual(b1.postcode_locator, b2.postcode_locator)
        self.assertEqual(b1.multi_occ_count, b2.multi_occ_count)

    def assertEqualApplicationCrossReference(self, a1, a2):
        self.assertEqual(a1.xref_key, a2.xref_key)
        self.assertEqual(a1.cross_reference, a2.cross_reference)
        self.assertEqual(a1.version, a2.version)
        self.assertEqual(a1.source, a2.source)
        self.assertEqual(a1.uprn, a2.uprn)
        self.assertEqual(a1.start_date, a2.start_date)
        self.assertEqual(a1.end_date, a2.end_date)
        self.assertEqual(a1.last_update_date, a2.last_update_date)
        self.assertEqual(a1.entry_date, a2.entry_date)

    def assertEqualLPI(self, l1, l2):
        self.assertEqual(l1.lpi_key, l2.lpi_key)
        self.assertEqual(l1.uprn, l2.uprn)
        self.assertEqual(l1.language, l2.language)
        self.assertEqual(l1.logical_status, l2.logical_status)
        self.assertEqual(l1.start_date, l2.start_date)
        self.assertEqual(l1.end_date, l2.end_date)
        self.assertEqual(l1.last_update_date, l2.last_update_date)
        self.assertEqual(l1.entry_date, l2.entry_date)
        self.assertEqual(l1.sao_start_number, l2.sao_start_number)
        self.assertEqual(l1.sao_start_suffix, l2.sao_start_suffix)
        self.assertEqual(l1.sao_end_number, l2.sao_end_number)
        self.assertEqual(l1.sao_end_suffix, l2.sao_end_suffix)
        self.assertEqual(l1.sao_text, l2.sao_text)
        self.assertEqual(l1.pao_start_number, l2.pao_start_number)
        self.assertEqual(l1.pao_start_suffix, l2.pao_start_suffix)
        self.assertEqual(l1.pao_end_number, l2.pao_end_number)
        self.assertEqual(l1.pao_end_suffix, l2.pao_end_suffix)
        self.assertEqual(l1.pao_text, l2.pao_text)
        self.assertEqual(l1.usrn, l2.usrn)
        self.assertEqual(l1.usrn_match_indicator, l2.usrn_match_indicator)
        self.assertEqual(l1.area_name, l2.area_name)
        self.assertEqual(l1.level, l2.level)
        self.assertEqual(l1.official_flag, l2.official_flag)

    def assertEqualDeliveryPointAddress(self, d1, d2):
        self.assertEqual(d1.rm_udprn, d2.rm_udprn)
        self.assertEqual(d1.uprn, d2.uprn)
        self.assertEqual(d1.parent_addressable_uprn, d2.parent_addressable_uprn)
        self.assertEqual(d1.organisation_name, d2.organisation_name)
        self.assertEqual(d1.department_name, d2.department_name)
        self.assertEqual(d1.sub_building_name, d2.sub_building_name)
        self.assertEqual(d1.building_name, d2.building_name)
        self.assertEqual(d1.building_number, d2.building_number)
        self.assertEqual(d1.dependent_thoroughfare_name, d2.dependent_thoroughfare_name)
        self.assertEqual(d1.thoroughfare_name, d2.thoroughfare_name)
        self.assertEqual(d1.double_dependent_locality, d2.double_dependent_locality)
        self.assertEqual(d1.dependent_locality, d2.dependent_locality)
        self.assertEqual(d1.post_town, d2.post_town)
        self.assertEqual(d1.postcode_index, d2.postcode_index)
        self.assertEqual(d1.postcode, d2.postcode)
        self.assertEqual(d1.postcode_type, d2.postcode_type)
        self.assertEqual(d1.welsh_dependent_thoroughfare_name, d2.welsh_dependent_thoroughfare_name)
        self.assertEqual(d1.welsh_thoroughfare_name, d2.welsh_thoroughfare_name)
        self.assertEqual(d1.welsh_double_dependent_locality, d2.welsh_double_dependent_locality)
        self.assertEqual(d1.welsh_dependent_locality, d2.welsh_dependent_locality)
        self.assertEqual(d1.welsh_post_town, d2.welsh_post_town)
        self.assertEqual(d1.po_box_number, d2.po_box_number)
        self.assertEqual(d1.process_date, d2.process_date)
        self.assertEqual(d1.start_date, d2.start_date)
        self.assertEqual(d1.end_date, d2.end_date)
        self.assertEqual(d1.last_update_date, d2.last_update_date)
        self.assertEqual(d1.entry_date, d2.entry_date)

    def assertEqualOrganisation(self, o1, o2):
        self.assertEqual(o1.org_key, o2.org_key)
        self.assertEqual(o1.organisation, o2.organisation)
        self.assertEqual(o1.legal_name, o2.legal_name)
        self.assertEqual(o1.uprn, o2.uprn)
        self.assertEqual(o1.start_date, o2.start_date)
        self.assertEqual(o1.end_date, o2.end_date)
        self.assertEqual(o1.last_update_date, o2.last_update_date)
        self.assertEqual(o1.entry_date, o2.entry_date)

    def assertEqualClassification(self, c1, c2):
        self.assertEqual(c1.class_key, c2.class_key)
        self.assertEqual(c1.uprn, c2.uprn)
        self.assertEqual(c1.classification_code, c2.classification_code)
        self.assertEqual(c1.class_scheme, c2.class_scheme)
        self.assertEqual(c1.scheme_version, c2.scheme_version)
        self.assertEqual(c1.start_date, c2.start_date)
        self.assertEqual(c1.end_date, c2.end_date)
        self.assertEqual(c1.last_update_date, c2.last_update_date)
        self.assertEqual(c1.entry_date, c2.entry_date)

    def test_full_and_delta(self):
        self._test_full()
        self._test_delta()

    def _test_full(self):
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
        self.assertEqualStreet(
            street, Street(
                usrn='18300001',
                record_type=constants.STREET_RECORD_TYPE_CODE.STREET_DESCRIPTION,
                swa_org_ref_naming='6805',
                state=constants.STREET_STATE_CODE.OPEN,
                state_date=date(year=1990, month=1, day=1),
                street_surface=constants.STREET_SURFACE_CODE.METALLED,
                street_classification=constants.STREET_CLASSIFICATION_CODE.ALL_VEHICLES,
                version='0',
                street_start_date=date(year=2003, month=12, day=3),
                street_end_date=date(year=2003, month=12, day=1),
                last_update_date=date(year=2011, month=9, day=21),
                record_entry_date=date(year=2003, month=12, day=3),
                street_start_coords=Point(
                    253837.00, 371990.00, srid=27700
                ),
                street_end_coords=Point(
                    254610.00, 372719.00, srid=27700
                ),
                street_tolerance=10
            )
        )

        # street descriptor
        self.assertEqual(StreetDescriptor.objects.count(), 2)
        sd = StreetDescriptor.objects.filter(
            language=constants.LANGUAGE_CODE.ENG
        )[0]
        self.assertEqualStreetDescriptor(sd, StreetDescriptor(
            sd_key='18300001ENG',
            usrn='18300001',
            street_description='description eng',
            locality_name='location eng',
            town_name='town_name eng',
            administrative_area='administrative area eng',
            language=constants.LANGUAGE_CODE.ENG
        ))

        # BLPU
        self.assertEqual(BLPU.objects.count(), 1)
        blpu = BLPU.objects.all()[0]
        self.assertEqualBLPU(blpu, BLPU(
            uprn='100020576017',
            logical_status=constants.LOGICAL_STATUS_CODE.APPROVED,
            blpu_state=constants.BLPU_STATE_CODE.UNDER_CONSTRUCTION,
            blpu_state_date=date(year=2000, month=11, day=22),
            parent_uprn='100020576016',
            coords=Point(530231.00, 159062.00, srid=27700),
            rpc=constants.RPC_CODE.VISUAL_CENTRE,
            local_custodian_code=5240,
            start_date=date(year=2001, month=3, day=19),
            end_date=date(year=2001, month=3, day=15),
            last_update_date=date(year=2001, month=3, day=13),
            entry_date=date(year=2001, month=3, day=12),
            postal_address=constants.POSTAL_ADDRESS_CODE.SINGLE,
            postcode_locator='SW1A 1AA',
            multi_occ_count=0
        ))

        # ApplicationCrossReference
        self.assertEqual(ApplicationCrossReference.objects.count(), 1)
        acr = ApplicationCrossReference.objects.all()[0]
        self.assertEqualApplicationCrossReference(acr,
            ApplicationCrossReference(
                xref_key="5240X900041534",
                cross_reference="osgb1000002148020239",
                version='3',
                source="7666MA",
                uprn='100020576017',
                start_date=date(year=2001, month=3, day=19),
                end_date=date(year=2001, month=3, day=18),
                last_update_date=date(year=2001, month=4, day=1),
                entry_date=date(year=2001, month=3, day=26),
            )
        )

        # LPI
        self.assertEqual(LPI.objects.count(), 1)
        lpi = LPI.objects.all()[0]
        self.assertEqualLPI(lpi, LPI(
            lpi_key="5240L000131331",
            uprn='100020576017',
            language="ENG",
            logical_status=constants.LOGICAL_STATUS_CODE.APPROVED,
            start_date=date(year=2000, month=3, day=19),
            end_date=date(year=2000, month=3, day=18),
            last_update_date=date(year=2001, month=4, day=1),
            entry_date=date(year=2000, month=3, day=23),
            sao_start_number="0",
            sao_start_suffix="aa",
            sao_end_number="11",
            sao_end_suffix="bb",
            sao_text="sao_text",
            pao_start_number="36",
            pao_start_suffix="cc",
            pao_end_number="22",
            pao_end_suffix="dd",
            pao_text="pao_text",
            usrn="20500302",
            usrn_match_indicator=constants.USRN_MATCH_INDICATOR_CODE.MATCHED_MANUALLY,
            area_name="area_name",
            level="level",
            official_flag=constants.OFFICIAL_FLAG_CODE.NO,
        ))

        # DeliveryPointAddress
        self.assertEqual(DeliveryPointAddress.objects.count(), 1)
        dpa = DeliveryPointAddress.objects.all()[0]
        self.assertEqualDeliveryPointAddress(dpa, DeliveryPointAddress(
            rm_udprn="5452552",
            uprn="100020576017",
            parent_addressable_uprn="100020576016",
            organisation_name="organisation_name",
            department_name="department_name",
            sub_building_name="sub_building_name",
            building_name="building_name",
            building_number=36,
            dependent_thoroughfare_name="dependent_thoroughfare_name",
            thoroughfare_name="thoroughfare_name",
            double_dependent_locality="double_dependent_locality",
            dependent_locality="dependent_locality",
            post_town="post_town",
            postcode_index="sw1a1aa",
            postcode="SW1A 1AA",
            postcode_type=constants.POSTCODE_TYPE_CODE.SMALL_USER,
            welsh_dependent_thoroughfare_name="welsh_dependent_thoroughfare_name",
            welsh_thoroughfare_name="welsh_thoroughfare_name",
            welsh_double_dependent_locality="welsh_double_dependent_locality",
            welsh_dependent_locality="welsh_dependent_locality",
            welsh_post_town="welsh_post_town",
            po_box_number="123456",
            process_date=date(year=2000, month=10, day=20),
            start_date=date(year=2000, month=3, day=19),
            end_date=date(year=2000, month=3, day=18),
            last_update_date=date(year=2000, month=4, day=1),
            entry_date=date(year=2000, month=3, day=26),
        ))

        # Organisation
        self.assertEqual(Organisation.objects.count(), 1)
        org = Organisation.objects.all()[0]
        self.assertEqualOrganisation(org, Organisation(
            org_key="5330O000078219",
            organisation="Org Name",
            legal_name="legal_name",
            uprn="10010197979",
            start_date=date(year=2000, month=8, day=20),
            end_date=date(year=2000, month=8, day=19),
            last_update_date=date(year=2010, month=10, day=24),
            entry_date=date(year=2000, month=8, day=10),
        ))

        # Classification
        self.assertEqual(Classification.objects.count(), 1)
        clazz = Classification.objects.all()[0]
        self.assertEqualClassification(clazz, Classification(
            class_key="5240C000041534",
            uprn="100020576017",
            classification_code="RD",
            class_scheme="Scheme",
            scheme_version="1.0",
            start_date=date(year=2000, month=3, day=19),
            end_date=date(year=2000, month=3, day=18),
            last_update_date=date(year=2000, month=4, day=1),
            entry_date=date(year=2000, month=3, day=26)
        ))

    def _test_delta(self):
        call_command(
            'import_addressbase_premium',
            os.path.join(os.path.dirname(__file__), 'data', 'delta'),
            **{
                'no_multiprocessing': True,
                'from': 1,
                'to': 999
            }
        )

        # street
        self.assertEqual(Street.objects.count(), 1)
        street = Street.objects.all()[0]
        self.assertEqualStreet(
            street, Street(
                usrn='18300001',
                record_type=constants.STREET_RECORD_TYPE_CODE.STREET_DESCRIPTION,
                swa_org_ref_naming='6806',
                state=constants.STREET_STATE_CODE.OPEN,
                state_date=date(year=1990, month=1, day=2),
                street_surface=constants.STREET_SURFACE_CODE.METALLED,
                street_classification=constants.STREET_CLASSIFICATION_CODE.ALL_VEHICLES,
                version='1',
                street_start_date=date(year=2003, month=12, day=4),
                street_end_date=date(year=2003, month=12, day=2),
                last_update_date=date(year=2011, month=9, day=22),
                record_entry_date=date(year=2003, month=12, day=4),
                street_start_coords=Point(
                    253838.00, 371991.00, srid=27700
                ),
                street_end_coords=Point(
                    254611.00, 372720.00, srid=27700
                ),
                street_tolerance=11
            )
        )

        # street descriptor
        self.assertEqual(StreetDescriptor.objects.count(), 1)
        sd = StreetDescriptor.objects.filter(
            language=constants.LANGUAGE_CODE.ENG
        )[0]
        self.assertEqualStreetDescriptor(sd, StreetDescriptor(
            sd_key='18300001ENG',
            usrn='18300001',
            street_description='description eng 1',
            locality_name='location eng 1',
            town_name='town_name eng 1',
            administrative_area='administrative area eng 1',
            language=constants.LANGUAGE_CODE.ENG
        ))

        # BLPU
        self.assertEqual(BLPU.objects.count(), 1)
        blpu = BLPU.objects.all()[0]
        self.assertEqualBLPU(blpu, BLPU(
            uprn='100020576017',
            logical_status=constants.LOGICAL_STATUS_CODE.APPROVED,
            blpu_state=constants.BLPU_STATE_CODE.UNDER_CONSTRUCTION,
            blpu_state_date=date(year=2000, month=11, day=23),
            parent_uprn='100020576017',
            coords=Point(530232.00, 159063.00, srid=27700),
            rpc=constants.RPC_CODE.VISUAL_CENTRE,
            local_custodian_code=5241,
            start_date=date(year=2001, month=3, day=20),
            end_date=date(year=2001, month=3, day=16),
            last_update_date=date(year=2001, month=3, day=14),
            entry_date=date(year=2001, month=3, day=13),
            postal_address=constants.POSTAL_ADDRESS_CODE.SINGLE,
            postcode_locator='SW1A 1AB',
            multi_occ_count=1
        ))

        # ApplicationCrossReference
        self.assertEqual(ApplicationCrossReference.objects.count(), 1)
        acr = ApplicationCrossReference.objects.all()[0]
        self.assertEqualApplicationCrossReference(acr,
            ApplicationCrossReference(
                xref_key="5240X900041534",
                cross_reference="osgb1000002148020240",
                version='4',
                source="7666MB",
                uprn='100020576017',
                start_date=date(year=2001, month=3, day=20),
                end_date=date(year=2001, month=3, day=19),
                last_update_date=date(year=2001, month=4, day=2),
                entry_date=date(year=2001, month=3, day=27),
            )
        )

        # LPI
        self.assertEqual(LPI.objects.count(), 1)
        lpi = LPI.objects.all()[0]
        self.assertEqualLPI(lpi, LPI(
            lpi_key="5240L000131331",
            uprn='100020576017',
            language="ENG",
            logical_status=constants.LOGICAL_STATUS_CODE.APPROVED,
            start_date=date(year=2000, month=3, day=20),
            end_date=date(year=2000, month=3, day=19),
            last_update_date=date(year=2001, month=4, day=2),
            entry_date=date(year=2000, month=3, day=24),
            sao_start_number="1",
            sao_start_suffix="ab",
            sao_end_number="12",
            sao_end_suffix="bc",
            sao_text="sao_text 1",
            pao_start_number="37",
            pao_start_suffix="cd",
            pao_end_number="23",
            pao_end_suffix="de",
            pao_text="pao_text 1",
            usrn="20500302",
            usrn_match_indicator=constants.USRN_MATCH_INDICATOR_CODE.MATCHED_MANUALLY,
            area_name="area_name 1",
            level="level 1",
            official_flag=constants.OFFICIAL_FLAG_CODE.NO,
        ))

        # DeliveryPointAddress
        self.assertEqual(DeliveryPointAddress.objects.count(), 1)
        dpa = DeliveryPointAddress.objects.all()[0]
        self.assertEqualDeliveryPointAddress(dpa, DeliveryPointAddress(
            rm_udprn="5452552",
            uprn="100020576017",
            parent_addressable_uprn="100020576017",
            organisation_name="organisation_name 1",
            department_name="department_name 1",
            sub_building_name="sub_building_name 1",
            building_name="building_name 1",
            building_number=37,
            dependent_thoroughfare_name="dependent_thoroughfare_name 1",
            thoroughfare_name="thoroughfare_name 1",
            double_dependent_locality="double_dependent_locality 1",
            dependent_locality="dependent_locality 1",
            post_town="post_town 1",
            postcode_index="sw1a1ab",
            postcode="SW1A 1AB",
            postcode_type=constants.POSTCODE_TYPE_CODE.SMALL_USER,
            welsh_dependent_thoroughfare_name="welsh_dependent_thoroughfare_name 1",
            welsh_thoroughfare_name="welsh_thoroughfare_name 1",
            welsh_double_dependent_locality="welsh_double_dependent_locality 1",
            welsh_dependent_locality="welsh_dependent_locality 1",
            welsh_post_town="welsh_post_town 1",
            po_box_number="123457",
            process_date=date(year=2000, month=10, day=21),
            start_date=date(year=2000, month=3, day=20),
            end_date=date(year=2000, month=3, day=19),
            last_update_date=date(year=2000, month=4, day=2),
            entry_date=date(year=2000, month=3, day=27),
        ))

        # Organisation
        self.assertEqual(Organisation.objects.count(), 1)
        org = Organisation.objects.all()[0]
        self.assertEqualOrganisation(org, Organisation(
            org_key="5330O000078219",
            organisation="Org Name 1",
            legal_name="legal_name 1",
            uprn="10010197979",
            start_date=date(year=2000, month=8, day=21),
            end_date=date(year=2000, month=8, day=20),
            last_update_date=date(year=2010, month=10, day=25),
            entry_date=date(year=2000, month=8, day=11),
        ))

        # Classification
        self.assertEqual(Classification.objects.count(), 1)
        clazz = Classification.objects.all()[0]
        self.assertEqualClassification(clazz, Classification(
            class_key="5240C000041534",
            uprn="100020576017",
            classification_code="RF",
            class_scheme="Scheme 1",
            scheme_version="2.0",
            start_date=date(year=2000, month=3, day=20),
            end_date=date(year=2000, month=3, day=19),
            last_update_date=date(year=2000, month=4, day=2),
            entry_date=date(year=2000, month=3, day=27)
        ))

