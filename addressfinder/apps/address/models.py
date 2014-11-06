import json

from django.contrib.gis.db import models

from .utils import AddressFormatter


class Address(models.Model):
    uprn = models.CharField(max_length=12, primary_key=True)
    os_address_toid = models.CharField(max_length=20, default='', blank=True)
    rm_udprn = models.CharField(max_length=8)
    organisation_name = models.CharField(max_length=60, default='', blank=True)
    department_name = models.CharField(max_length=60, default='', blank=True)
    po_box_number = models.CharField(max_length=6, default='', blank=True)
    building_name = models.CharField(max_length=50, default='', blank=True)
    sub_building_name = models.CharField(max_length=30, default='', blank=True)
    building_number = models.PositiveSmallIntegerField(null=True, blank=True)
    dependent_thoroughfare_name = models.CharField(
        max_length=80, default='', blank=True)
    thoroughfare_name = models.CharField(max_length=80, default='', blank=True)
    post_town = models.CharField(max_length=30, default='', blank=True)
    double_dependent_locality = models.CharField(
        max_length=35, default='', blank=True)
    dependent_locality = models.CharField(
        max_length=35, default='', blank=True)
    point = models.PointField()
    postcode = models.CharField(max_length=8)
    postcode_index = models.CharField(max_length=7, db_index=True)
    postcode_type = models.CharField(max_length=1)
    rpc = models.PositiveSmallIntegerField()
    change_type = models.CharField(max_length=1)
    start_date = models.DateField()
    last_update_date = models.DateField()
    entry_date = models.DateField()
    primary_class = models.CharField(max_length=1)
    process_date = models.DateField()

    objects = models.GeoManager()

    def __unicode__(self):
        return u"%s - %s" % (self.uprn, self.postcode)

    class Meta:
        verbose_name_plural = 'addresses'
        ordering = ['building_number', 'building_name', 'sub_building_name']

    @property
    def formatted_address(self):
        return AddressFormatter.format(self)
