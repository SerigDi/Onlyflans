from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import ContactForm


class ContactFormForm(forms.Form):
    # contact_form_uuid No necesita ser declarado en nuestro form
    customer_name = forms.CharField(
        max_length=64, label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    customer_email = forms.EmailField(
        label='Correo',
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))


class ContactFormModelForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['customer_name', 'customer_email', 'message']
        labels = {
            'customer_name': 'Nombre',
            'customer_email': 'Correo',
            'message': 'Mensaje',
        }
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
