from django.db import models
from databaseFunctions.models import product

# Create your models here.
class facilities(models.Model):
    facilityChoices = [
        ('aaa', 'null')
    ]
    facilityLocation = models.CharField(max_length=3, choices=facilityChoices, default='aaa')

class productHistory(models.Model):
    class Meta:
        unique_together = (('productDate', 'productID'),)
    productDate = models.DateField(auto_now=False, auto_now_add=True)
    productID = models.ForeignKey(product, on_delete=models.CASCADE)
    facilityID = models.ForeignKey(facilities, on_delete=models.CASCADE)
    openingBalance = models.IntegerField()
    forecastedUsage = models.IntegerField(null=True)


