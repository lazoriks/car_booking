"""
URL configuration for car_booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
#from .views import booking_view, store_booking, get_booking, delete_booking
from .views import booking_view, store_booking, get_booking, delete_booking, custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('booking/', views.booking, name='booking'),

    path('accounts/', include('allauth.urls')),
    path('store_booking/', store_booking, name='store_booking'),
    path('get_booking/<int:booking_id>/', get_booking, name='get_booking'),
    path('delete_booking/<int:booking_id>/', delete_booking, name='delete_booking'),
]

# Додаємо обробник 404 помилок
handler404 = custom_404