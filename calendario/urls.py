from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CalendarioViewSet

router = DefaultRouter()
router.register(r'calendario', CalendarioViewSet, basename='calendario')

urlpatterns = [
    path('', include(router.urls)),
]
