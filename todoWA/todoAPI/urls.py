from django.urls import path

from . import views

urlpatterns = [
    path('login/',views.loginView,name='loginView'),
    path('logout/',views.logoutView,name='logoutView')
]