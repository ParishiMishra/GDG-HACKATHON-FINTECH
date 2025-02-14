from django import forms
from .models import Portfolio, Investment

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name', 'goal_amount', 'risk_tolerance']

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['symbol', 'quantity', 'purchase_price', 'purchase_date']