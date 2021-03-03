from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginuser, name='loginuser'),
    path('signup/', views.signupuser, name='signupuser'),

]
