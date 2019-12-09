from django.db import models

# Create your models here.
from django.db import models

class document(models.Model):
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

class statuses (models.Model):
    statusID = models.CharField(max_length=5, primary_key=True)
    status = models.CharField(max_length=50)

class locations (models.Model):
    locationID = models.CharField(max_length=10, primary_key=True)
    locationName = models.CharField(max_length=100)

class categories (models.Model):
    productCategoryID = models.IntegerField(primary_key=True)
    productCategory = models.CharField(max_length=50)

class product (models.Model): # Instantiating each Field in the Database Table
    masterPN = models.CharField(max_length=10, primary_key=True)
    amendedPN = models.CharField(max_length=10)
    gaiaPN = models.CharField(max_length=10)
    SgPN = models.CharField(max_length=40)
    supplementaryPN = models.CharField(max_length=40)
    description = models.TextField()
    productCategoryID = models.ForeignKey(categories, on_delete=models.CASCADE)
    isManual = models.BooleanField()
    filmThickness = models.IntegerField()
    statusID = models.ForeignKey(statuses, on_delete=models.CASCADE)
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

class productStockStatus (models.Model):
    MasterPN = models.ForeignKey(product, on_delete=models.CASCADE)
    locationID = models.ForeignKey(locations, on_delete=models.CASCADE)
    value = models.IntegerField()
    supplierID = models.ForeignKey(suppliers, on_delete=models.CASCADE)