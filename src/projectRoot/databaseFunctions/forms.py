from django import forms

from .models import document

class documentForm(forms.ModelForm):
    class Meta:
        model = document
        fields = ('name', 'document')
        
