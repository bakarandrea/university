from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('scan/', views.scan, name='scan'),
    path('api/scan/', views.api_scan, name='api_scan'),
    path('report/generate/', views.generate_report, name='generate_report'),
]
