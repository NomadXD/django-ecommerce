from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.product_catalog, name='product_catalog'),
]