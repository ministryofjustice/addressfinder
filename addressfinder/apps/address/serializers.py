from .models import DeliveryPointAddress

from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer


class DeliveryPointAddressSerializer(GeoModelSerializer):
    formatted_address = serializers.Field(source='formatted_address')

    def __init__(self, *args, **kwargs):
        super(DeliveryPointAddressSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].QUERY_PARAMS.get('fields')

        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = DeliveryPointAddress
        fields = ('uprn', 'organisation_name', 'department_name',
                  'po_box_number', 'building_name', 'sub_building_name',
                  'building_number', 'thoroughfare_name',
                  'dependent_thoroughfare_name', 'dependent_locality',
                  'double_dependent_locality', 'post_town', 'postcode',
                  'postcode_type', 'formatted_address')
