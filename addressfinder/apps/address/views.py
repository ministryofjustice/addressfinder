# import json

from rest_framework import viewsets
# from rest_framework import generics
# from rest_framework import status
# from rest_framework.response import Response

from .models import DeliveryPointAddress
from .serializers import DeliveryPointAddressSerializer


class DeliveryPointAddressViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeliveryPointAddress.objects.all()
    serializer_class = DeliveryPointAddressSerializer

    def get_queryset(self):
        postcode = self.request.QUERY_PARAMS.get('postcode', '').\
            replace(' ', '').lower()

        return self.queryset.filter(postcode_index=postcode)


# class PostcodeView(generics.RetrieveAPIView):
#     def get(self, request, *args, **kwargs):
#         postcode = kwargs.get('postcode', '').replace(' ', '').lower()

#         geom = DeliveryPointAddress.objects.filter(
#             postcode_index=postcode).collect(field_name='point')

#         if geom:
#             return Response(json.loads(geom.centroid.geojson),
#                             status=status.HTTP_200_OK)

#         return Response(None, status=status.HTTP_404_NOT_FOUND)
