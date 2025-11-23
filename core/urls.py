from django.urls import path
from .views import index, calendario_view, admin_dashboard_view

urlpatterns = [
    path('', index, name='index'),
    path('calendario/', calendario_view, name='calendario'),
    path('admin-dashboard/', admin_dashboard_view, name='admin_dashboard'),
]
