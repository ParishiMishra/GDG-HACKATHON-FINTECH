from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    goal_amount = models.FloatField()
    risk_tolerance = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Investment(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)  # e.g., AAPL for Apple stock
    quantity = models.FloatField()
    purchase_price = models.FloatField()
    purchase_date = models.DateField()

    def __str__(self):
        return f"{self.symbol} - {self.quantity} shares"

# Create your models here.
