from django.contrib import admin
from django.urls import path
from processos import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard_distribuicao, name='dashboard'),
]