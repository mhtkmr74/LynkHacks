from django.db import models
from location_field.models.plain import PlainLocationField

# Create your models here.


class Victims(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField()
    area = models.CharField(max_length=255)
    requirement_status = models.IntegerField(default=0, null=True)
    location = PlainLocationField(based_fields=['city'], zoom=7)


    def __str__(self):
        return self.name

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def summary(self):
        return self.body[:100]

    class Meta:
        db_table = 'Victims'
