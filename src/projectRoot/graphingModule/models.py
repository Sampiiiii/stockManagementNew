from django.db import models
from databaseFunctions.models import product

# Create your models here.
class Facilities(models.Model):
    FacilityChoices = [
        ('aaa', 'null')
    ]
    FacilityLocation = models.CharField(max_length=3, choices=FacilityChoices, default='aaa')

class productHistory(models.Model):
    class Meta:
        unique_together = (('productDate', 'productID'),)
    productDate = models.DateField(auto_now=False, auto_now_add=True)
    productID = models.ForeignKey(product, on_delete=models.CASCADE)
    FacilityID = models.ForeignKey(Facilities, on_delete=models.CASCADE)
    OpeningBalance = models.IntegerField()
    ForecastedUsage = models.IntegerField(null=True)


