from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('links/', views.links, name='links'),
    path('wiki/', views.wiki, name='wiki'),
    path('product_insert/', views.product_insert, name='product_insert'),
    path('db_schema/', views.db_schema, name='db_schema'),
    path('product_list/', views.product_list, name='product_list'),
]
 