from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('search/', views.search_stock, name='search_stock'),
    path('buy/<int:stock_id>/', views.buy_stock, name='buy_stock'),
    path('sell/<int:stock_id>/', views.sell_stock, name='sell_stock'),
    path('transactions/', views.transaction_history, name='transaction_history'),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
