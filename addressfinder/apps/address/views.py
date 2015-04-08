import json

from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .models import Address
from .serializers import AddressSerializer


class AddressViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        postcode = self.request.QUERY_PARAMS.get('postcode', '').\
            replace(' ', '').lower()

        return self.queryset.filter(postcode_index=postcode)


class PostcodeView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        postcode = kwargs.get('postcode', '').replace(' ', '').lower()

        geom = Address.objects.filter(
            postcode_index=postcode).collect(field_name='point')

        if geom:
            return Response(json.loads(geom.centroid.geojson),
                            status=status.HTTP_200_OK)

        return Response(None, status=status.HTTP_404_NOT_FOUND)

class PartialPostcodeView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        # NOTE: we add on a space and lookup the value in the formatted postcode field,
        #       NOT the postcode_index, to allow us to differentiate, say, 
        #       N1 from N11, N12, etc
        postcode = kwargs.get('postcode', '').replace(' ', '').upper()

        geom = Address.objects.filter(
            postcode__startswith=postcode + ' ').collect(field_name='point')

        if geom:
            return Response(json.loads(geom.centroid.geojson),
                            status=status.HTTP_200_OK)

        return Response(None, status=status.HTTP_404_NOT_FOUND)