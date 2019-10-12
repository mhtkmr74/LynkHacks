from django.db import models
from location_field.models.spatial import LocationField

# Create your models here.
class Victims(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField()
    area = models.CharField(max_length=255)
    need = models.TextField()
    location = LocationField(based_fields=['area'], zoom=7, default=Point(1.0, 1.0))
    

    def __str__(self):
        return self.name

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def summary(self):
        return self.body[:100]
