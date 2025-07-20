from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_view, name='register'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('hizmet-sec/', views.service_choice_view, name='hizmet_sec'),
    path('tahlil/', views.tahlil_view, name='tahlil_sayfasi'),
    path('oneriler/', views.oneriler_view, name='oneriler_sayfasi'),
    path('hatirlatici/', views.hatirlatici_view, name='hatirlatici_sayfasi'),
    path('soru/', views.soru_view, name='soru_sayfasi'),
    path('profil/', views.profile_view, name='profile'),
]