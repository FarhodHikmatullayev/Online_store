from django import forms

from products.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'image', 'price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            "placeholder": "name...",
            "class": 'form-control',
        })
        self.fields['category'].widget.attrs.update({
            "class": 'form-control',
        })
        self.fields['image'].widget.attrs.update({
            "class": 'form-control',
        })
        self.fields['price'].widget.attrs.update({
            "placeholder": 'price..',
            "class": 'form-control',

        })


class QuantityForm(forms.Form):
    quantity = forms.IntegerField(
        label='Quantity',
        initial=1,
        min_value=1,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control short-input'})
    )
