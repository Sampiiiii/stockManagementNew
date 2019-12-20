from django import forms

from .models import document, product

class documentForm(forms.ModelForm):
    class Meta:
        model = document
        fields = ('name', 'document')
  
class productForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ('primaryKey', 'amendedPN', 'gaiaPN', 'SgPN', 'supplementaryPN',
        'description', 'productCategory', 'isManual', 'filmThickness',
        'status', 'cylinderSequence', 'sealingSequence', 'USDCostPrice',
        'deliveredDutyGBP', 'gaiaSellPrice', 'samuelGrantPurchasePrice', 'samuelGrantBuyback',
        'PCSPerObject', 'amountPerPallet', 'minimumOrderQuantity', 'deflatedWidth',
        'deflatedLength', 'deflatedHeight', 'inflatedWidth', 'inflatedLength', 'inflatedHeight',
        'CTNAmountPerPallet', 'CTNWidth', 'CTNLength', 'CTNHeight', 'netWeight', 'grossWeight')
