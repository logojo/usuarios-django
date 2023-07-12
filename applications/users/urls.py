from django.urls import path

from . import views 

app_name = "users_app"

urlpatterns = [
    path('users/register', views.Register.as_view(), name='register'),
    path('users/verify/<pk>/', views.CodeVerify.as_view(), name='verify'),
    path('users/login', views.Login.as_view(), name='login'),
    path('users/logout', views.Logout.as_view(), name='logout'),
    path('users/update', views.UpdatePassword.as_view(), name='update'),
]
