from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('generate_product/', views.generate_random_product, name='generate_product'),
    path('db_schema/', views.db_schema, name='db_schema'),
    path('about/', views.about, name='about'),
    path('showcase', views.ShowcaseView.as_view(), name='showcase'),
    path('base/', views.base, name='base'),
    path('careers/', views.careers, name='careers'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)