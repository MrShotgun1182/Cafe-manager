from django import forms
from .models import MenuItem

class OrderForm(forms.Form):
    table_number = forms.IntegerField(label="شماره میز")
    items = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.filter(is_available=True),
        widget=forms.CheckboxSelectMultiple,
        label="انتخاب محصولات"
    )