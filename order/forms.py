from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user_name', 'phone_number', 'address', 'comment', 'delivery_method', 'email']
        labels = {'user_name': 'Ваше имя', 'phone_number': 'Телефон', 'address': 'Адрес доставки'}
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'delivery_method': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

