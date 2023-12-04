from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.login_user, name="login_user"),
    path('auth/', views.get_user, name="auth"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('delete/user', views.delete_user, name="delete_user"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('schedule/<str:date_url>', views.schedule, name="schedule"),
    path('schedule/delete/<int:id>', views.delete_schedule, name="delete_schedule"),
    path('services/', views.get_services, name="services"),
    path('services/delete/<int:id>/', views.delete_service, name="delete_service"),
    path('available_times/<str:username>/<slug:service>/<str:date_url>', views.get_available_times, name="available_times"),
    path('operating_days/<str:date_url>', views.get_operating_days, name="operating_days"),
    path('days-with-schedule/<str:date_url>', views.get_days_with_schedule, name="days_with_schedule"),
    path('settings/', views.get_settings, name="settings"),
    path('settings/profile', views.update_profile, name="update_profile"),
    path('settings/company', views.update_company, name="update_company"),
    path('settings/company/delete-photo-profile', views.delete_photo_profile, name="delete_photo_profile"),
    path('settings/category', views.update_category, name="update_category"),
    path('settings/address', views.update_address, name="update_address"),
    path('settings/schedule', views.get_settings_schedule, name="settings_schedule"),
    path('settings/schedule/update', views.update_schedule, name="update_schedule"),
    path('settings/schedule/delete/<int:id>/', views.delete_interval, name="delete_interval"),
    path('professional/<str:username>', views.get_page, name="get_page"),
    path('professional/<str:username>/<str:service>/<str:date>', views.get_details_date, name="get_date"),
    path('professional/<str:username>/<str:service>/<str:date_url>/<str:time>', views.get_client, name="get_client")


]
