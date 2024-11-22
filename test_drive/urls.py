from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_booking_and_request, name='booking_view'),
    path('report/', views.report_view, name='report'),
    path('login/', views.login_or_register, name='login'),
    path('edit/<str:model_name>/<int:record_id>/', views.edit_record, name='edit_record'),
]
