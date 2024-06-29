from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('links/', views.links, name='links'),
    path('wiki/', views.wiki, name='wiki'),
]
 