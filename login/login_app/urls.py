from django.urls import path

from . import views

app_name = "login_app"
urlpatterns = [
    path('', views.index, name='index'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]