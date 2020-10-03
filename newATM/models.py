from django.db import models


class Atm(models.Model):
    id = models.IntegerField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    region = models.CharField(max_length=100)
    region_type = models.CharField(max_length=100)
    settlement_type = models.CharField(max_length=100)
    settlement = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    full_address = models.CharField(max_length=250)

    def __str__(self):
        return self.id