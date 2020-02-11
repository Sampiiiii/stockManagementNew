from django import forms

from .models import facilities, productHistory

# Forms Here

class facilityForm(forms.ModelForm):

    class Meta:
        model = facilities
        fields = ('facilityLocation', )

class productHistoryForm(forms.ModelForm):

    class Meta:
        model = productHistory
        fields = ('productID', 'facilityID', 
        'openingBalance', 'forecastedUsage')
