from django.test import TestCase

from address.models import Address
from address.utils import AddressFormatter


class AddressFormatterTestCase(TestCase):

    def test_simple_address(self):
        a = Address(
            building_number=16,
            thoroughfare_name='VIXEN ROAD',
            post_town='BRADDOCK',
            postcode='KT6 5BT'
        )

        self.assertEqual(
            AddressFormatter.format(a),
            u'16 Vixen Road\nBraddock\nKT6 5BT'
        )

    def test_first_last_building_name_chars_numeric(self):
        a = Address(
            building_name='1-2',
            thoroughfare_name='NURSERY LANE',
            dependent_locality='PENN',
            post_town='HIGH WYCOMBE',
            postcode='HP10 8LS'
        )

        self.assertEqual(
            AddressFormatter.format(a),
            u'1-2 Nursery Lane\nPenn\nHigh Wycombe\nHP10 8LS'
        )

    def test_first_penultimate_building_name_chars_numeric_last_alpha(self):
        a = Address(
            building_name='12A',
            thoroughfare_name='UPPERKIRKGATE',
            post_town='ABERDEEN',
            postcode='AB10 1BA'
        )

        self.assertEqual(
            AddressFormatter.format(a),
            u'12A Upperkirkgate\nAberdeen\nAB10 1BA'
        )

    def test_one_char_building_name(self):
        a = Address(
            building_name='K',
            thoroughfare_name='PORTLAND ROAD',
            post_town='DORKING',
            postcode='RH4 1EW'
        )

        self.assertEqual(
            AddressFormatter.format(a),
            u'K, Portland Road\nDorking\nRH4 1EW'
        )

    def test_organisation_name(self):
        a = Address(
            organisation_name='LEDA ENGINEERING LTD',
            dependent_locality='APPLEFORD',
            post_town='ABINGDON',
            postcode='OX14 4PG'
        )

        self.assertEqual(
            AddressFormatter.format(a),
            u'Leda Engineering Ltd\nAppleford\nAbingdon\nOX14 4PG'
        )

    def test_building_name_exception_with_dependent_thoroughfare(self):
        a = Address(
            building_name='1A',
            dependent_thoroughfare_name='SEASTONE COURT',
            thoroughfare_name='STATION ROAD',
            post_town='HOLT',
            postcode='NR25 7HG'
        )

        self.assertEqual(
            AddressFormatter.format(a),
            u'1A Seastone Court\nStation Road\nHolt\nNR25 7HG'
        )

    def test_building_name_only(self):
        a = Address(
            building_name='THE MANOR',
            thoroughfare_name='UPPER HILL',
            post_town='HORLEY',
            postcode='RH6 0HP'
        )

        self.assertEqual(
            AddressFormatter.format(a),
            u'The Manor\nUpper Hill\nHorley\nRH6 0HP'
        )

    # PAF docs table 26c
    # def test_building_name_only_ends_with_number_range(self):
    #     a = Address(
    #         organisation_name='S D ALCOTT FLORISTS',
    #         building_name='FLOWER HOUSE 189A',
    #         thoroughfare_name='PYE GREEN ROAD',
    #         post_town='CANNOCK',
    #         postcode='WS11 5SB'
    #     )

    #     self.assertEqual(
    #         AddressFormatter.format(a),
    #         u'S D Alcott Florists\nFlower House\n189A Pye Green Road\nCannock\nWS11 5SB'
    #     )

    def test_building_name_only_ends_with_simple_number(self):
        a = Address(
            organisation_name='JAMES VILLA HOLIDAYS',
            building_name='CENTRE 30',
            thoroughfare_name='ST. LAURENCE AVENUE',
            post_town='GRAFTON',
            postcode='ME16 0LP'
        )

        self.assertEqual(
            AddressFormatter.format(a),
            u'James Villa Holidays\nCentre 30\nSt. Laurence Avenue\nGrafton\nME16 0LP'
        )

    def test_building_name_and_building_number(self):
        a = Address(
            building_name='VICTORIA HOUSE',
            building_number=15,
            thoroughfare_name='THE STREET',
            post_town='CHRISTCHURCH',
            postcode='BH23 6AA'
        )

        self.assertEqual(
            AddressFormatter.format(a),
            u'Victoria House\n15 The Street\nChristchurch\nBH23 6AA'
        )

    def test_sub_building_name_and_building_number(self):
        a = Address(
            sub_building_name='FLAT 1',
            building_number=12,
            thoroughfare_name='LIME TREE AVENUE',
            post_town='BRISTOL',
            postcode='BS8 4AB'
        )

        self.assertEqual(
            AddressFormatter.format(a),
            u'Flat 1\n12 Lime Tree Avenue\nBristol\nBS8 4AB'
        )

    # PAF docs table 28B
    # no addresses in the current PAF seem to require this formatting
    # def test_sub_building_name_and_building_name(self):
    #     a = Address(
    #         sub_building_name='A',
    #         building_number=12,
    #         thoroughfare_name='HIGH STREET NORTH',
    #         dependent_locality='COOMBE BISSETT',
    #         post_town='SALISBURY',
    #         postcode='SP5 4NA'
    #     )

    #     self.assertEqual(
    #         AddressFormatter.format(a),
    #         u'12A High Street North\nCoombe Bissett\nSalisbury\nSP5 4NA'
    #     )

    def test_numeric_sub_building_name_and_building_name_and_building_number_exception(self):
        a = Address(
            sub_building_name='10B',
            building_name='BARRY JACKSON TOWER',
            thoroughfare_name='ESTONE WALK',
            post_town='BIRMINGHAM',
            postcode='B6 5BA'
        )

        self.assertEqual(
            AddressFormatter.format(a),
            u'10B Barry Jackson Tower\nEstone Walk\nBirmingham\nB6 5BA'
        )

    def test_numeric_sub_building_name_and_building_name_and_building_number(self):
        a = Address(
            sub_building_name='STABLES FLAT',
            building_name='THE MANOR',
            thoroughfare_name='UPPER HILL',
            post_town='HORLEY',
            postcode='RH6 0HP'
        )

        self.assertEqual(
            AddressFormatter.format(a),
            u'Stables Flat\nThe Manor\nUpper Hill\nHorley\nRH6 0HP'
        )

    def test_alpha_sub_building_name_and_building_name_and_building_number_exception(self):
        a = Address(
            sub_building_name='2B',
            building_name='THE TOWER',
            building_number=27,
            thoroughfare_name='JOHN STREET',
            post_town='WINCHESTER',
            postcode='SO23 9AP',
        )

        self.assertEqual(
            AddressFormatter.format(a),
            u'2B The Tower\n27 John Street\nWinchester\nSO23 9AP'
        )

    def test_alpha_sub_building_name_and_building_name_and_building_number(self):
        a = Address(
            sub_building_name='BASEMENT FLAT',
            building_name='VICTORIA HOUSE',
            building_number=15,
            thoroughfare_name='THE STREET',
            post_town='CORYTON',
            postcode='BP23 6AA'
        )

        self.assertEqual(
            AddressFormatter.format(a),
            u'Basement Flat\nVictoria House\n15 The Street\nCoryton\nBP23 6AA'
        )
