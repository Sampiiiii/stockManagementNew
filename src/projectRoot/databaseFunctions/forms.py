from django import forms

from .models import document, product

class documentForm(forms.ModelForm):
    class Meta:
        model = document
        fields = ('name', 'document')
  
class productForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ('amendedPN', 'GAIAPN', 'SgPN', 'supplementaryPN',
        'description', 'productCategory', 'isManual', 'filmThickness',
        'status', 'cylinderSequence', 'sealingSequence', 'CP',
        'DDP', 'GAIASP', 'SGPP', 'SGBB', 'PCSPerRoll', 'PCSPerPallet', 'MOQ', 'deflatedWidth',
        'deflatedLength', 'deflatedHeight', 'inflatedWidth', 'inflatedLength', 'inflatedHeight',
        'CTNAmountPerPallet', 'CTNWidth', 'CTNLength', 'CTNHeight', 'nettWeight', 'grossWeight')
