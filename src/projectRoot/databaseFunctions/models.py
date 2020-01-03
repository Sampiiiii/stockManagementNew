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
        return self.supplierID + ',' + self.supplierName

class locations (models.Model):
    locationID = models.CharField(max_length=10, primary_key=True)
    locationName = models.CharField(max_length=100)

    def __str__(self):
        return self.locationID + ',' + self.locationName
    
class product (models.Model): # Populated First
    #id = models.AutoField(primary_key=True)
    amendedPN = models.CharField(max_length=30, blank=True)
    GAIAPN = models.CharField(max_length=30, blank=True)
    SgPN = models.CharField(max_length=40, blank=True)
    supplementaryPN = models.CharField(max_length=40, blank=True)
    description = models.TextField(blank=True)
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
    filmThickness = models.IntegerField(blank=True)
    statuses_choices = [
        ('A', 'Active'),
    ]
    STATUS = models.CharField(max_length=1, choices=statuses_choices, default='A')
    cylinderSequence = models.CharField(max_length=30, blank=True)
    sealingSequence = models.CharField(max_length=30, blank=True)
    CP = models.FloatField(max_length=8, blank=True)
    DDP = models.FloatField(max_length=8, blank=True)
    GAIASP = models.FloatField(max_length=8, blank=True)
    SGPP = models.FloatField(max_length=8, blank=True)
    SGBB = models.IntegerField(blank=True)
    PCSPerRoll = models.IntegerField(blank=True)
    PCSPerPallet = models.IntegerField(blank=True)
    MOQ = models.IntegerField(blank=True)
    deflatedWidth = models.IntegerField(blank=True)
    deflatedLength = models.IntegerField(blank=True)
    deflatedHeight = models.IntegerField(blank=True)
    inflatedWidth = models.IntegerField(blank=True)
    inflatedLength = models.IntegerField(blank=True)
    inflatedHeight = models.IntegerField(blank=True)
    CTNAmountPerPallet = models.IntegerField(blank=True)
    CTNWidth = models.IntegerField(blank=True)
    CTNLength = models.IntegerField(blank=True)
    CTNHeight = models.IntegerField(blank=True)
    nettWeight = models.FloatField(max_length=5, blank=True)
    grossWeight = models.FloatField(max_length=5, blank=True)

    def __str__(self):
        return self.masterPN + ',' +self.description

class productStockStatus (models.Model): #Generated Later
    MasterPN = models.ForeignKey(product, on_delete=models.CASCADE)
    locationID = models.ForeignKey(locations, on_delete=models.CASCADE)
    value = models.IntegerField()
    supplierID = models.ForeignKey(suppliers, on_delete=models.CASCADE)

    def __str__(self):
        return self.MasterPN + ',' + self.value