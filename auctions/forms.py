from django import forms
from .models import Listing

class ItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    class Meta:
        model = Listing
        fields = [
            'name',
            'current_price',
            'desc',
            'image',
            'tags']