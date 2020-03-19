from django.urls import path

from . import views

urlpatterns = [
    path('login/',views.loginView,name='loginView'),
    path('logout/',views.logoutView,name='logoutView'),
    path('todos/',views.TodoController.as_view()),
    path('todos/<int:todoid>',views.TodoControllerSpecific.as_view()),
]