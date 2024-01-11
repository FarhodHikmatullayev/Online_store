from django import forms

from products.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'photo', 'price')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            "placeholder": "name...",
            "class": 'form-control',
        })
        self.fields['photo'].widget.attrs.update({
            "class": 'form-control',
        })
        self.fields['price'].widget.attrs.update({
            "placeholder": 'price..',
            "class": 'form-control',

        })
