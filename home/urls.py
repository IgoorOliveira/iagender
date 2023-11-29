from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.login_user, name="login_user"),
    path('auth/', views.get_user, name="auth"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('schedule', views.schedule, name="schedule"),
    path('services/', views.get_services, name="services"),
    path('operating_days/', views.get_operating_days, name="operating_days"),
    path('settings/', views.get_settings, name="settings"),
    path('settings/profile', views.update_profile, name="update_profile"),
    path('settings/company', views.update_company, name="update_company"),
    path('settings/category', views.update_category, name="update_category"),
    path('settings/address', views.update_address, name="update_address"),
    path('settings/schedule', views.get_settings_schedule, name="settings_schedule"),
    path('settings/schedule/update', views.update_schedule, name="update_schedule"),
    path('settings/schedule/delete/<int:id>/', views.delete_interval, name="delete_interval"),
    path('teste/', views.get_page, name="get_page"),
    path('teste/date', views.teste_date, name="teste-date"),
    path('teste/user', views.teste_user, name="teste-user")


]
