from django.contrib.gis.db import models

from .utils import DeliveryPointAddressFormatter
from . import constants


class BLPU(models.Model):
    """
    Definition - a BLPU is defined as a real-world object that is an 'area of
    land, property or structure of fixed location having uniform occupation,
    ownership or function'. The BLPU is the core element of AddressBase Premium.
    In essence, a BLPU associates a real-world object on the ground to a UPRN.
    """
    uprn = models.CharField(max_length=12, primary_key=True)
    logical_status = models.PositiveSmallIntegerField(
        choices=constants.LOGICAL_STATUS_CODE.CHOICES
    )
    blpu_state = models.PositiveSmallIntegerField(
        choices=constants.BLPU_STATE_CODE.CHOICES, null=True, blank=True
    )
    blpu_state_date = models.DateField(null=True, blank=True)
    parent_uprn = models.CharField(max_length=12, blank=True)  # fk to self
    coords = models.PointField()
    rpc = models.PositiveSmallIntegerField(
        choices=constants.RPC_CODE.CHOICES
    )
    local_custodian_code = models.PositiveSmallIntegerField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    last_update_date = models.DateField()
    entry_date = models.DateField()
    postal_address = models.CharField(
        choices=constants.POSTAL_ADDRESS_CODE.CHOICES, max_length=1
    )
    postcode_locator = models.CharField(max_length=8)
    multi_occ_count = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return u'%s' % self.uprn


class Classification(models.Model):
    """
    Definition - a structured text entry that provides the code for
    the type of BLPU and the classification scheme from which the
    code is taken.
    """
    class_key = models.CharField(max_length=14, primary_key=True)
    uprn = models.CharField(max_length=12)  # fk to BLPU
    classification_code = models.CharField(max_length=6)
    class_scheme = models.CharField(max_length=60)
    scheme_version = models.CharField(max_length=5)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    last_update_date = models.DateField()
    entry_date = models.DateField()

    def __unicode__(self):
        return u'%s (code %s)' % (self.uprn, self.classification_code)


class DeliveryPointAddress(models.Model):
    """
    Definition - a Delivery Point Address is defined as a property that
    receives deliveries from Royal Mail.
    """
    # NOTE: not sure that rm_udprn is really the pk
    rm_udprn = models.CharField(max_length=8, primary_key=True)
    uprn = models.CharField(max_length=12)  # fk to BLPU
    parent_addressable_uprn = models.CharField(max_length=12, blank=True)  # fk to BLPU
    organisation_name = models.CharField(max_length=60, blank=True)
    department_name = models.CharField(max_length=60, blank=True)
    sub_building_name = models.CharField(max_length=30, blank=True)
    building_name = models.CharField(max_length=50, blank=True)
    building_number = models.PositiveSmallIntegerField(null=True, blank=True)
    dependent_thoroughfare_name = models.CharField(max_length=80, blank=True)
    thoroughfare_name = models.CharField(max_length=80, blank=True)
    double_dependent_locality = models.CharField(max_length=35, blank=True)
    dependent_locality = models.CharField(max_length=35, blank=True)
    post_town = models.CharField(max_length=30)
    postcode_index = models.CharField(max_length=7, db_index=True)
    postcode = models.CharField(max_length=8)
    postcode_type = models.CharField(
        choices=constants.POSTCODE_TYPE_CODE.CHOICES, max_length=1
    )
    welsh_dependent_thoroughfare_name = models.CharField(max_length=80, blank=True)
    welsh_thoroughfare_name = models.CharField(max_length=80, blank=True)
    welsh_double_dependent_locality = models.CharField(max_length=35, blank=True)
    welsh_dependent_locality = models.CharField(max_length=35, blank=True)
    welsh_post_town = models.CharField(max_length=30, blank=True)
    po_box_number = models.CharField(max_length=6, blank=True)
    process_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    last_update_date = models.DateField()
    entry_date = models.DateField()

    def __unicode__(self):
        return u"%s - %s" % (self.rm_udprn, self.postcode)

    @property
    def formatted_address(self):
        return DeliveryPointAddressFormatter.format(self)


class LPI(models.Model):
    """
    Definition - an LPI is a structured text entry that identifies a BLPU.
    """
    lpi_key = models.CharField(max_length=14, primary_key=True)
    uprn = models.CharField(max_length=12)  # fk to BLPU
    language = models.CharField(
        choices=constants.LANGUAGE_CODE.CHOICES, max_length=3
    )
    logical_status = models.PositiveSmallIntegerField(
        choices=constants.LOGICAL_STATUS_CODE.CHOICES
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    last_update_date = models.DateField()
    entry_date = models.DateField()
    sao_start_number = models.CharField(max_length=4, blank=True)
    sao_start_suffix = models.CharField(max_length=2, blank=True)
    sao_end_number = models.CharField(max_length=4, blank=True)
    sao_end_suffix = models.CharField(max_length=2, blank=True)
    sao_text = models.CharField(max_length=90, blank=True)
    pao_start_number = models.CharField(max_length=4, blank=True)
    pao_start_suffix = models.CharField(max_length=2, blank=True)
    pao_end_number = models.CharField(max_length=4, blank=True)
    pao_end_suffix = models.CharField(max_length=2, blank=True)
    pao_text = models.CharField(max_length=90, blank=True)
    usrn = models.CharField(max_length=8)  # fk to Street
    usrn_match_indicator = models.CharField(
        choices=constants.USRN_MATCH_INDICATOR_CODE.CHOICES,
        max_length=1
    )
    area_name = models.CharField(max_length=35, blank=True)
    level = models.CharField(max_length=30, blank=True)
    official_flag = models.CharField(
        choices=constants.OFFICIAL_FLAG_CODE.CHOICES,
        max_length=1, blank=True
    )

    def __unicode__(self):
        return u"%s - %s - %s" % (self.lpi_key, self.uprn, self.usrn)


class Organisation(models.Model):
    """
    Definition - a structured text entry identifying the name of the
    current occupier on the fascia of the BLPU.
    """
    org_key = models.CharField(max_length=14, primary_key=True)
    organisation = models.CharField(max_length=100)
    legal_name = models.CharField(max_length=60, blank=True)
    uprn = models.CharField(max_length=12)  # fk to BLPU
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    last_update_date = models.DateField()
    entry_date = models.DateField()

    def __unicode__(self):
        return u"%s - %s: %s" % (self.org_key, self.uprn. self.organisation)


class ApplicationCrossReference(models.Model):
    """
    Definition - the application cross references contain a lookup
    between the UPRN and the unique identifiers of other relevant datasets.
    """
    xref_key = models.CharField(max_length=14, primary_key=True)
    cross_reference = models.CharField(max_length=50)
    version = models.CharField(max_length=3, blank=True)
    source = models.CharField(max_length=6)
    uprn = models.CharField(max_length=12)  #fk to BLPU
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    last_update_date = models.DateField()
    entry_date = models.DateField()

    def __unicode__(self):
        return u"%s - %s - (%s:%s)" % (
            self.xref_key, self.uprn,
            self.source, self.cross_reference
        )


class Street(models.Model):
    """
    Definition - a way or thoroughfare providing a right of passage on
    foot, by cycle or by motor vehicle, or access to more than one property.
    """
    usrn = models.CharField(max_length=12, primary_key=True)
    record_type = models.PositiveSmallIntegerField(
        choices=constants.STREET_RECORD_TYPE_CODE.CHOICES
    )
    swa_org_ref_naming = models.CharField(max_length=4)
    state = models.PositiveSmallIntegerField(
        choices=constants.STREET_STATE_CODE.CHOICES,
        null=True, blank=True
    )
    state_date = models.DateField(null=True, blank=True)
    street_surface = models.PositiveSmallIntegerField(
        choices=constants.STREET_SURFACE_CODE.CHOICES,
        null=True, blank=True
    )
    street_classification = models.PositiveSmallIntegerField(
        choices=constants.STREET_CLASSIFICATION_CODE.CHOICES,
        null=True, blank=True
    )
    version = models.CharField(max_length=3)
    street_start_date = models.DateField()
    street_end_date = models.DateField(null=True, blank=True)
    last_update_date = models.DateField()
    record_entry_date = models.DateField()
    street_start_coords = models.PointField()
    street_end_coords = models.PointField()
    street_tolerance = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return u"%s" % self.usrn


class StreetDescriptor(models.Model):
    """
    Definition - a descriptive identifier providing a reference
    for the street in the form of its location.

    Note: no fixed pk. The pk is really (usrn, language)
        so building one == usrn + language
    """
    sd_key = models.CharField(max_length=15, primary_key=True)  # == usrn + language
    usrn = models.CharField(max_length=12)  # fk to Street
    street_description = models.CharField(max_length=100)
    locality_name = models.CharField(max_length=35, blank=True)
    town_name = models.CharField(max_length=30, blank=True)
    administrative_area = models.CharField(max_length=30)
    language = models.CharField(
        choices=constants.LANGUAGE_CODE.CHOICES, max_length=3
    )

    def __unicode__(self):
        return u"%s: %s" % (self.usrn, self.street_description)

    class Meta:
        unique_together = (("usrn", "language"),)


class SuccessorRecord(models.Model):
    """
    Definition - this record holds references to a UPRN and to any replacement
    UPRN, for example, if a building is split into two sub-buildings;
    the sub-building UPRNS will be referenced in the successor field.
    """
    succ_key = models.CharField(max_length=14, primary_key=True)
    uprn = models.CharField(max_length=12)  # fk to BLPU
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    last_update_date = models.DateField()
    entry_date = models.DateField()
    successor = models.CharField(max_length=12)  # fk to BLPU

    def __unicode__(self):
        return u"%s - %s successor %s" % (
            self.succ_key, self.uprn, self.successor
        )


# TODO metadata
