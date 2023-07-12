from django.urls import path

from . import views 

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('mixin', views.PrueabaMixin.as_view(), name='mixin'),
]
