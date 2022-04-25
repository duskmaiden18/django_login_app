from django.urls import path

from . import views

app_name = "login_app"
urlpatterns = [
    path('', views.index, name='index'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('log_out/', views.log_out, name='log_out'),
]
