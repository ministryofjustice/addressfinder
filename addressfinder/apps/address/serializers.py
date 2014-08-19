from .models import Address

from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    point = serializers.Field(source='point_geojson_dict')
    formatted_address = serializers.Field(source='formatted_address')

    class Meta:
        model = Address
        fields = ('uprn', 'organisation_name', 'department_name',
                  'po_box_number', 'building_name', 'sub_building_name',
                  'building_number', 'thoroughfare_name',
                  'dependent_thoroughfare_name', 'dependent_locality',
                  'double_dependent_locality', 'post_town', 'postcode',
                  'postcode_type', 'formatted_address', 'point')
