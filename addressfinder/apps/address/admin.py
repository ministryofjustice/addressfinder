from django.contrib.gis import admin

from .models import BLPU, Street, Classification, DeliveryPointAddress, \
    LPI, Organisation, ApplicationCrossReference, StreetDescriptor, \
    SuccessorRecord


admin.site.register(BLPU, admin.OSMGeoAdmin)
admin.site.register(Classification)
admin.site.register(DeliveryPointAddress)
admin.site.register(LPI)
admin.site.register(Organisation)
admin.site.register(ApplicationCrossReference)
admin.site.register(Street, admin.OSMGeoAdmin)
admin.site.register(StreetDescriptor)
admin.site.register(SuccessorRecord)
