from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.login_user, name="login_user"),
    path('auth/', views.get_user, name="auth"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('services/', views.get_services, name="services"),
    path('operating_days/', views.get_operating_days, name="operating_days"),
    path('settings/', views.get_settings, name="settings")
]
