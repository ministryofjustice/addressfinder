from django.contrib.gis.db import models


AREA_TYPE_CHOICES = (
    ('POL', 'Police'),
)


class Area(models.Model):
    name = models.CharField(max_length=255)
    area_type = models.CharField(max_length=3, db_index=True,
                                 choices=AREA_TYPE_CHOICES)
    geom = models.MultiPolygonField()

    objects = models.GeoManager()

    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.area_type)
