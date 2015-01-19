from .models import Area

from rest_framework_gis.serializers import GeoModelSerializer


class AreaSerializer(GeoModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name', 'area_type')
