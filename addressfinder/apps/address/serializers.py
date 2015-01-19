from .models import Address
from areas.serializers import AreaSerializer

from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer


class AddressSerializer(GeoModelSerializer):
    formatted_address = serializers.Field(source='formatted_address')
    police_areas = AreaSerializer()

    def __init__(self, *args, **kwargs):
        super(AddressSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].QUERY_PARAMS.get('fields')

        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Address
        fields = ('uprn', 'organisation_name', 'department_name',
                  'po_box_number', 'building_name', 'sub_building_name',
                  'building_number', 'thoroughfare_name',
                  'dependent_thoroughfare_name', 'dependent_locality',
                  'double_dependent_locality', 'post_town', 'postcode',
                  'postcode_type', 'formatted_address', 'point',
                  'police_areas')
