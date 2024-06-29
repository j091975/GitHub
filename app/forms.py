# store/forms.py

from django import forms
from .models import product

class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ['product_id', 'sku', 'name', 'description', 'price', 'quantity', 'location', 'DateAdded', 'DateUpdated']