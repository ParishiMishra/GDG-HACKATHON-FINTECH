from django.shortcuts import render
from .models import Portfolio, Investment
import requests

ALPHA_VANTAGE_API_KEY = '3YCCC7YIBIR1POWY'

def get_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data

def dashboard(request):
    portfolios = Portfolio.objects.filter(user=request.user)
    portfolio_data = []

    for portfolio in portfolios:
        investments = Investment.objects.filter(portfolio=portfolio)
        total_value = 0
        total_cost = 0
        investment_data = []

        for investment in investments:
            stock_data = get_stock_data(investment.symbol)
            current_price = float(list(stock_data['Time Series (5min)'].values())[0]['1. open'])
            current_value = current_price * investment.quantity
            total_value += current_value
            total_cost += investment.purchase_price * investment.quantity
            investment_data.append({
                'symbol': investment.symbol,
                'quantity': investment.quantity,
                'purchase_price': investment.purchase_price,
                'current_price': current_price,
                'current_value': current_value,
                'roi': ((current_value - (investment.purchase_price * investment.quantity)) / (investment.purchase_price * investment.quantity)) * 100,
            })

        portfolio_roi = ((total_value - total_cost) / total_cost) * 100 if total_cost != 0 else 0
        portfolio_data.append({
            'portfolio': portfolio,
            'investments': investment_data,
            'total_value': total_value,
            'total_cost': total_cost,
            'portfolio_roi': portfolio_roi,
        })

    return render(request, 'portfolio/dashboard.html', {'portfolio_data': portfolio_data})