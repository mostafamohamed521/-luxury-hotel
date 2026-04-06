from django import forms

class PaymentForm(forms.Form):
    METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
    ]
    method = forms.ChoiceField(choices=METHOD_CHOICES)
    card_number = forms.CharField(max_length=19, min_length=16)
    card_name = forms.CharField(max_length=100)
    expiry = forms.CharField(max_length=5)
    cvv = forms.CharField(max_length=4, min_length=3)

    def clean_card_number(self):
        num = self.cleaned_data['card_number'].replace(' ', '').replace('-', '')
        if not num.isdigit():
            raise forms.ValidationError("Enter a valid card number.")
        return num

    def clean_expiry(self):
        exp = self.cleaned_data['expiry']
        if '/' not in exp:
            raise forms.ValidationError("Enter expiry as MM/YY.")
        return exp
