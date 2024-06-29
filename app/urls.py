from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('links/', views.links, name='links'),
    path('wiki/', views.wiki, name='wiki'),
    path('product_insert/', views.product_insert, name='product_insert'),
    path('db_schema/', views.db_schema, name='db_schema'),
    path('product_list/', views.product_list, name='product_list'),
    path('generate_product/', views.generate_random_product, name='generate_product'),
    path('generate_products/success/<int:num_products>/', views.generate_product_success, name='generate_products_success'),
]
 