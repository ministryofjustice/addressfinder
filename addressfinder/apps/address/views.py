import json

from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Address
from .serializers import AddressSerializer


class AddressViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        postcode = self.request.QUERY_PARAMS.get('postcode', '').\
            replace(' ', '').lower()

        return self.queryset.filter(postcode_index=postcode)


class PostcodeView(ListAPIView):
    def get(self, request, *args, **kwargs):
        postcode = kwargs.get('postcode', '').replace(' ', '').lower()

        addresses = Address.objects.filter(postcode_index=postcode)

        if addresses.count() == 0:
            return Response('', status=status.HTTP_404_NOT_FOUND)

        resp = addresses.collect(field_name='point').centroid.geojson

        return Response(json.loads(resp), status=status.HTTP_200_OK)
