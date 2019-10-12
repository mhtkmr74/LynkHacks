from django.db import models
from location_field.models.plain import PlainLocationField
# Create your models here.


class Victims(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    number = models.IntegerField(default=None, null=True)
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


class Needs(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=60)
    sub_type = models.CharField(max_length=60)

    class Meta:
        db_table = 'Needs'


class Requirements(models.Model):
    id = models.AutoField(primary_key=True)
    victim_id = models.ForeignKey(Victims, on_delete=models.CASCADE, db_column='Victim_id')
    requirement = models.ForeignKey(Needs, on_delete=models.CASCADE, db_column='Need_id')
    delivery_status = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    quantity = models.IntegerField(default=0)


class SafeLocations(models.Model):
    id = models.AutoField(primary_key=True)
    latitude = models.FloatField(default=None, null=True)
    longitude = models.FloatField(default=None, null=True)

    class Meta:
        db_table = 'SafeLocations'

