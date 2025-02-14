from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Portfolio, Investment
from .forms import PortfolioForm, InvestmentForm
import requests

ALPHA_VANTAGE_API_KEY = '3YCCC7YIBIR1POWY'

def get_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data

@login_required
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

        # Calculate portfolio progress
        if portfolio.goal_amount > 0:
            progress = (total_value / portfolio.goal_amount) * 100
            if progress > 100:
                progress = 100  # Ensure it doesn't exceed 100%
        else:
            progress = 0  # If goal_amount is 0, set progress to 0

        portfolio_roi = ((total_value - total_cost) / total_cost) * 100 if total_cost != 0 else 0
        portfolio_data.append({
            'portfolio': portfolio,
            'investments': investment_data,
            'total_value': total_value,
            'total_cost': total_cost,
            'portfolio_roi': portfolio_roi,
            'progress': progress,  # Add progress to the context
        })

    return render(request, 'portfolio/dashboard.html', {'portfolio_data': portfolio_data})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect('dashboard')  # Redirect to the dashboard
    else:
        form = UserCreationForm()
    return render(request, 'portfolio/signup.html', {'form': form})

@login_required
def add_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            return redirect('dashboard')
    else:
        form = PortfolioForm()
    return render(request, 'portfolio/add_portfolio.html', {'form': form})

@login_required
def add_investment(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.portfolio = portfolio
            investment.save()
            return redirect('dashboard')
    else:
        form = InvestmentForm()
    return render(request, 'portfolio/add_investment.html', {'form': form, 'portfolio': portfolio})