import json

from django.contrib.gis.db import models
from extended_choices import Choices


class Address(models.Model):

    CHANGE_TYPE_CODES = Choices(
        ('INSERT', 'I', 'Insert'),
        ('UPDATE', 'U', 'Update'),
        ('DELETE', 'D', 'Delete')
    )

    LANGUAGE_CODES = Choices(
        ('ENGLISH', 'ENG', 'English'),
        ('CYMRAEG', 'CYM', 'Cymraeg'),
        ('GAELIC', 'GAE', 'Gaelic')
    )

    POSTAL_ADDRESS_CODES = Choices(
        ('SINGLE', 'S', 'Single address'),
        ('NOT_POSTAL', 'N', 'Not a postal address'),
        ('CHILD', 'C', 'Multiple-occupancy or child address'),
        ('PARENT', 'M', 'Parent address with at least one child')
    )

    POSTCODE_TYPE_CODES = Choices(
        ('SMALL', 'S', 'Small user'),
        ('LARGE', 'L', 'Large user')
    )

    RPC_CODES = Choices(
        ('VISUAL_CENTRE', 1, 'Visual centre'),
        ('GENERAL_INTERNAL', 2, 'General internal point'),
        ('GRID_SW', 3, 'SW corner of referenced 100m grid'),
        ('STREET', 4, 'Start of referenced street'),
        ('POSTCODE', 5, 'General point based on postcode unit'),
        ('AUTHORITY_CENTRE', 9, 'Centre of contributing authority area'),
    )

    STATE_CODES = Choices(
        ('UNDER_CONSTRUCTION', 1, 'Under construction'),
        ('IN_USE', 2, 'In use'),
        ('UNOCCUPIED', 3, 'Unoccupied'),
        ('DEMOLISHED', 4, 'Demolished'),
        ('PERMISSION_GRANTED', 6, 'Planning permission granted')
    )

    USRN_MATCH_INDICATOR_CODES = Choices(
        ('MANUAL', 1, 'Matched manually to nearest accessible street'),
        ('SPATIAL', 2, 'Matched spatially to nearest USRN'),
    )

    uprn = models.BigIntegerField(primary_key=True)
    rm_udprn = models.IntegerField(blank=True, null=True)
    change_type = models.CharField(
        max_length=1, choices=CHANGE_TYPE_CODES.CHOICES)
    state = models.PositiveSmallIntegerField(
        null=True, blank=True, db_index=True, choices=STATE_CODES.CHOICES)
    state_date = models.DateField(null=True, blank=True)
    classification = models.CharField(max_length=6)
    parent_uprn = models.BigIntegerField(null=True, blank=True)
    point = models.PointField()
    rpc = models.PositiveSmallIntegerField(choices=RPC_CODES.CHOICES)
    local_custodian_code = models.PositiveSmallIntegerField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    last_update_date = models.DateField()
    entry_date = models.DateField()
    organisation_name = models.CharField(max_length=60, default='', blank=True)
    organisation = models.CharField(max_length=100, default='', blank=True)
    department_name = models.CharField(max_length=60, default='', blank=True)
    scottish_department_name = models.CharField(
        max_length=60, default='', blank=True)
    building_name = models.CharField(max_length=50, default='', blank=True)
    sub_building_name = models.CharField(max_length=30, default='', blank=True)
    sao_start_number = models.PositiveSmallIntegerField(null=True, blank=True)
    sao_start_suffix = models.CharField(max_length=2, default='', blank=True)
    sao_end_number = models.PositiveSmallIntegerField(null=True, blank=True)
    sao_end_suffix = models.CharField(max_length=2, default='', blank=True)
    sao_text = models.CharField(max_length=90, default='', blank=True)
    alt_language_sao_text = models.CharField(
        max_length=90, default='', blank=True)
    pao_start_number = models.PositiveSmallIntegerField(null=True, blank=True)
    pao_start_suffix = models.CharField(max_length=2, default='', blank=True)
    pao_end_number = models.PositiveSmallIntegerField(null=True, blank=True)
    pao_end_suffix = models.CharField(max_length=2, default='', blank=True)
    pao_text = models.CharField(max_length=90, default='', blank=True)
    alt_language_pao_text = models.CharField(
        max_length=90, default='', blank=True)
    usrn = models.PositiveIntegerField()
    usrn_match_indicator = models.CharField(
        max_length=1, choices=USRN_MATCH_INDICATOR_CODES.CHOICES)
    area_name = models.CharField(max_length=35, default='', blank=True)
    level = models.CharField(max_length=30, default='', blank=True)
    official_flag = models.NullBooleanField()
    os_address_toid = models.CharField(max_length=20, default='', blank=True)
    os_address_toid_version = models.PositiveSmallIntegerField(
        null=True, blank=True)
    os_roadlink_toid = models.CharField(max_length=20, default='', blank=True)
    os_roadlink_toid_version = models.PositiveSmallIntegerField(
        null=True, blank=True)
    os_topo_toid = models.CharField(max_length=20, default='', blank=True)
    os_topo_toid_version = models.PositiveSmallIntegerField(
        null=True, blank=True)
    voa_ct_record = models.BigIntegerField(null=True, blank=True)
    voa_ndr_record = models.BigIntegerField(null=True, blank=True)
    street_description = models.CharField(max_length=100)
    alt_language_street_description = models.CharField(
        max_length=100, default='', blank=True)
    dependent_thoroughfare_name = models.CharField(
        max_length=80, default='', blank=True)
    thoroughfare_name = models.CharField(max_length=80, default='', blank=True)
    welsh_dependent_thoroughfare_name = models.CharField(
        max_length=80, default='', blank=True)
    welsh_thoroughfare_name = models.CharField(
        max_length=80, default='', blank=True)
    double_dependent_locality = models.CharField(
        max_length=35, default='', blank=True)
    dependent_locality = models.CharField(
        max_length=35, default='', blank=True)
    locality_name = models.CharField(
        max_length=35, default='', blank=True)
    welsh_double_dependent_locality = models.CharField(
        max_length=35, default='', blank=True)
    welsh_dependent_locality = models.CharField(
        max_length=35, default='', blank=True)
    town_name = models.CharField(max_length=30, default='', blank=True)
    administrative_area = models.CharField(
        max_length=30, default='', blank=True)
    post_town = models.CharField(max_length=35, default='', blank=True)
    postcode = models.CharField(max_length=8)
    postcode_index = models.CharField(max_length=7, db_index=True)
    postcode_locator = models.CharField(max_length=8)
    postcode_type = models.CharField(
        max_length=1, choices=POSTCODE_TYPE_CODES.CHOICES, blank=True)
    postal_address = models.CharField(
        max_length=1, choices=POSTAL_ADDRESS_CODES.CHOICES)
    po_box_number = models.CharField(max_length=6, default='', blank=True)
    ward_code = models.CharField(max_length=9, default='', blank=True)
    parish_code = models.CharField(max_length=9, default='', blank=True)
    process_date = models.DateField(null=True, blank=True)
    multi_occ_count = models.PositiveSmallIntegerField(null=True, blank=True)
    voa_ndr_p_desc_code = models.CharField(
        max_length=5, default='', blank=True)
    voa_ndr_scat_code = models.CharField(max_length=4, default='', blank=True)
    alt_language = models.CharField(
        max_length=3, default='', blank=True, choices=LANGUAGE_CODES.CHOICES)

    objects = models.GeoManager()

    class Meta:
        verbose_name_plural = 'addresses'

    def __unicode__(self):
        name = "%s - %s" % (self.uprn, self.location_postcode)
        if self.postcode == '':
            name += ' (approx.)'
        return name

    @property
    def point_geojson_dict(self):
        return json.loads(self.point.geojson)

    @property
    def location_postcode(self):
        return self.postcode if self.postcode != '' else self.postcode_locator
