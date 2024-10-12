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
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import TemplateView

from . import views
from .sitemaps import StaticViewSitemap
from .views import store_booking, get_booking, delete_booking, custom_404, booking

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('booking/', booking, name='booking_view'),

    path('accounts/', include('allauth.urls')),
    path('store_booking/', store_booking, name='store_booking'),
    path('get_booking/<int:booking_id>/', get_booking, name='get_booking'),
    path('delete_booking/<int:booking_id>/', delete_booking, name='delete_booking'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

handler404 = custom_404