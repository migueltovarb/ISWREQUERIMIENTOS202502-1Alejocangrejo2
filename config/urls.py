from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from reservas.views import ReservaViewSet
from equipos.views import EquipoViewSet, LaboratorioViewSet, MantenimientoViewSet
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import routers
from reservas.views import ReservaViewSet
from equipos.views import EquipoViewSet, LaboratorioViewSet
from core import views as core_views

# Router para las APIs REST
router = routers.DefaultRouter()
router.register(r'reservas', ReservaViewSet)
router.register(r'equipos', EquipoViewSet)
router.register(r'laboratorios', LaboratorioViewSet)

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),
    
    # APIs REST
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    
    # Autenticación
    path('login/', core_views.login_view, name='login'),
    path('logout/', core_views.logout_view, name='logout'),
    
    # Vistas de templates
    path('', core_views.index, name='index'),
    path('calendario/', core_views.calendario, name='calendario'),
    path('mis-reservas/', core_views.mis_reservas, name='mis_reservas'),
    path('admin-dashboard/', core_views.admin_dashboard, name='admin_dashboard'),
    path('gestion-equipos/', core_views.gestion_equipos, name='gestion_equipos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
