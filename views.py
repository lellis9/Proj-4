from django.shortcuts import render


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Stock, Holding, Transaction
from .forms import UserRegisterForm
import requests

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'portfolio.html', {'form': form})

@login_required
def portfolio(request):
    holdings = Holding.objects.filter(user=request.user)
    return render(request, 'portfolio/portfolio.html', {'holdings': holdings})

@login_required
def search_stock(request):
    if request.method == 'POST':
        symbol = request.POST['symbol']
        response = requests.get(f'https://financial-api.com/stock/{symbol}')
        data = response.json()
        stock, created = Stock.objects.get_or_create(symbol=symbol, defaults={'name': data['name']})
        return render(request, 'portfolio/stock_detail.html', {'stock': stock, 'data': data})
    return render(request, 'portfolio/search_stock.html')

@login_required
def buy_stock(request, stock_id):
    stock = Stock.objects.get(id=stock_id)
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        price = float(request.POST['price'])
        total_cost = quantity * price
        profile = request.user.profile
        if profile.balance >= total_cost:
            profile.balance -= total_cost
            profile.save()
            holding, created = Holding.objects.get_or_create(user=request.user, stock=stock)
            holding.quantity += quantity
            holding.save()
            Transaction.objects.create(user=request.user, stock=stock, quantity=quantity, price=price, transaction_type='buy')
            return redirect('portfolio')
    return render(request, 'portfolio/buy_stock.html', {'stock': stock})

@login_required
def sell_stock(request, stock_id):
    stock = Stock.objects.get(id=stock_id)
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        price = float(request.POST['price'])
        profile = request.user.profile
        holding = Holding.objects.get(user=request.user, stock=stock)
        if holding.quantity >= quantity:
            holding.quantity -= quantity
            holding.save()
            profile.balance += quantity * price
            profile.save()
            Transaction.objects.create(user=request.user, stock=stock, quantity=quantity, price=price, transaction_type='sell')
            return redirect('portfolio')
    return render(request, 'portfolio/sell_stock.html', {'stock': stock})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'portfolio/transaction_history.html', {'transactions': transactions})
