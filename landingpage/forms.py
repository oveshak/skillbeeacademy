from django import forms
from .models import ExtraCharges, Product, Purchase

class PurchaseForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=True,
        label="Select Products"
    )
    extra_charges = forms.ModelMultipleChoiceField(
        queryset=ExtraCharges.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label="Select Extra Charges"
    )

    class Meta:
        model = Purchase
        fields = ['name', 'address', 'phone_number', 'payment_status', 'products', 'extra_charges']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'সম্পূর্ণ নাম লিখুন'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'বাড়ির নাম্বার, রোড, উপজেলা, জেলা'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '১১ ডিজিটের মোবাইল নাম্বার লিখুন'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
        }
