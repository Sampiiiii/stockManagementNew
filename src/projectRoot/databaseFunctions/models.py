from django.db import models

# Create your models here.
from django.db import models

class document(models.Model): # File storing module
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    document = models.FileField(upload_to='documents')
    
    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.document.delete()
        super().delete(*args, **kwargs)

class suppliers (models.Model):
    supplierID = models.CharField(max_length=10, primary_key=True)
    supplierName = models.CharField(max_length=100)
    supplierNumber = models.IntegerField()
    supplierEmail = models.CharField(max_length=254)
    companyNumber = models.CharField(max_length=50)

    def __str__(self):
        return self.supplierName

class locations (models.Model):
    locationID = models.CharField(max_length=10, primary_key=True)
    locationName = models.CharField(max_length=100)

    def __str__(self):
        return self.locationName
    
class product (models.Model): # Populated First
    masterPN = models.CharField(max_length=10, primary_key=True)
    amendedPN = models.CharField(max_length=10)
    gaiaPN = models.CharField(max_length=10)
    SgPN = models.CharField(max_length=40)
    supplementaryPN = models.CharField(max_length=40)
    description = models.TextField()
    category_choices = [
        ('aaa', 'null'),
        ('ASH', 'AIR|SHIELD™'),
        ('AMA', 'AIR|MAT™'),
        ('APA', 'AIR|PAKK™'),
        ('CCA', 'Corr Case '),
        ('TCO', 'TRANS|COVER'),
        ('TCA', 'TRANS|CASE '),
    ]
    productCategory = models.CharField(max_length=3, choices=category_choices, default='aaa')
    isManual = models.BooleanField()
    filmThickness = models.IntegerField()
    statuses_choices = [
        ('A', 'Active'),
    ]
    status = models.CharField(max_length=1, choices=statuses_choices, default='A')
    cylinderSequence = models.CharField(max_length=30)
    sealingSequence = models.CharField(max_length=30)
    USDCostPrice = models.FloatField(max_length=8)
    deliveredDutyGBP = models.FloatField(max_length=8)
    gaiaSellPrice = models.FloatField(max_length=8)
    samuelGrantPurchasePrice = models.FloatField(max_length=8)
    samuelGrantBuyback = models.IntegerField()
    PCSPerObject = models.IntegerField()
    amountPerPallet = models.IntegerField()
    minimumOrderQuantity = models.IntegerField()
    deflatedWidth = models.IntegerField()
    deflatedLength = models.IntegerField()
    deflatedHeight = models.IntegerField()
    inflatedWidth = models.IntegerField()
    inflatedLength = models.IntegerField()
    inflatedHeight = models.IntegerField()
    CTNAmountPerPallet = models.IntegerField()
    CTNWidth = models.IntegerField()
    CTNLength = models.IntegerField()
    CTNHeight = models.IntegerField()
    netWeight = models.FloatField(max_length=5)
    grossWeight = models.FloatField(max_length=5)

    def __str__(self):
        return self.masterPN + self.description

class productStockStatus (models.Model): #Generated Later
    MasterPN = models.ForeignKey(product, on_delete=models.CASCADE)
    locationID = models.ForeignKey(locations, on_delete=models.CASCADE)
    value = models.IntegerField()
    supplierID = models.ForeignKey(suppliers, on_delete=models.CASCADE)

    def __str__(self):
        return self.value