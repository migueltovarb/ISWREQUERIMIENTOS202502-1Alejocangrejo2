from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    """Vista de login con diseño Warframe"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Sesión iniciada correctamente')
            return redirect('index')
        else:
            messages.error(request, 'Credenciales inválidas')
    
    return render(request, 'login.html')

def logout_view(request):
    """Cerrar sesión"""
    auth_logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('login')

@login_required
def index(request):
    """Página principal"""
    return render(request, 'index.html')

@login_required
def calendario(request):
    """Vista del calendario"""
    return render(request, 'calendario.html')

@login_required
def mis_reservas(request):
    """Vista de mis reservas"""
    return render(request, 'mis_reservas.html')

@login_required
def admin_dashboard(request):
    """Dashboard de administración"""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('index')
    return render(request, 'admin_dashboard.html')

@login_required
def gestion_equipos(request):
    """Gestión de equipos (admin)"""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('index')
    return render(request, 'gestion_equipos.html')
