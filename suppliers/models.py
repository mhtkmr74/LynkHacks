from django.db import models
from location_field.models.plain import PlainLocationField

# Create your models here.


class Suppliers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    number = models.IntegerField()
    email = models.EmailField(max_length=60)
    area = models.CharField(max_length=255)
    need = models.TextField()
    location = PlainLocationField(based_fields=['city'], zoom=7)
    MEDICAL = 'ME'
    TRANSPORTATION = 'TR'
    WORKFORCE = 'WF'
    VOLUNTEER_CHOICES = [
        (MEDICAL, 'Medical'),
        (TRANSPORTATION, 'Transportation'),
        (WORKFORCE, 'WorkForce'),
    ]
    volunteer_type = models.CharField(
        max_length=2,
        choices=VOLUNTEER_CHOICES,
        default=WORKFORCE,
    )

    def is_upperclass(self):
        return self.volunteer_type in (self.MEDICAL, self.TRANSPORTATION, self.WORKFORCE)

    def __str__(self):
        return self.name

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def summary(self):
        return self.body[:100]

    class Meta:
        db_table = 'Suppliers'
