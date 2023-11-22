from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('auth/', views.auth_with_email, name="auth"),
    path('dashboard/', views.get_user, name="dashboard"),
    path('services/', views.get_services, name="services"),
    path('operating_days/', views.get_operating_days, name="operating_days")
]
