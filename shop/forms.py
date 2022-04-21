from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div


PAYMENT_CHOICES = (
    ('P', 'Paypal'),
    ('C', 'Credit card')
)


class CheckoutForm(forms.Form):
    first_name = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'placeholder': 'First name'
    }))
    surname = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'placeholder': 'Last name'
    }))
    address1 = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'placeholder': 'Street'
    }))
    address2 = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment'
    }))
    city = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'placeholder': 'City'
    }))
    postal = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'placeholder': 'Zip code'
    }))
    payment_method = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-4'),
                Column('surname', css_class='form-group col-4')
            ),
            Row(
                Column('address1', css_class='form-group col-4'),
                Column('address2', css_class='form-group col-4')
            ),
            Row(
                Column('city', css_class='form-group col-4'),
                Column('postal', css_class='form-group col-4')
            ),
            Column('payment_method', css_class='form-group col-10')

        )
        self.helper.form_tag = False


