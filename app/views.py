import os
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.db import connection
from .models import product, SoccerPlayer, Slide, Supplier, Order, OrderDetail, Customer, Warehouse_Products
from .forms import ProductForm  # Assuming you have a form for the Product
import random
import string
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import pandas as pd
from django.views import View
#from sklearn.datasets import load_iris
#from sklearn.datasets import make_moons
from sklearn.datasets import fetch_california_housing
#import matplotlib.pyplot as plt
from django.conf import settings

def generate_random_location():
    # Randomly choose one of 'AND', 'BAS', 'SAL'
    prefix = random.choice(['AND', 'BAS', 'SAL'])
    
    # Generate a random two-digit number between '01' and '99'
    number_part = '{:02}'.format(random.randint(1, 99))
    
    # Generate a random uppercase letter
    letter_part = random.choice(string.ascii_uppercase)
    
    # Combine all parts to form the location string
    location = f"{prefix}-{number_part}-{letter_part}"
    
    return location

def home(request):
    return render(request, 'app/home.html')

def base(request):
    return render(request, 'app/base.html')

def wiki(request):
    return render(request, 'app/wiki.html')

def links(request):
    return render(request, 'app/links.html')

def careers(request):
    return render(request, 'app/careers.html')

def about(request):
    slides = Slide.objects.all()  # Fetch all slides from database
    return render(request, 'app/about.html', {'slides': slides})

def product_insert(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('product_insert')  # Redirect to a list of products or a success page
    else:
        form = ProductForm()

    return render(request, 'app/product_insert.html', {'form': form})

def db_schema(request):
    schema_data = []

    with connection.cursor() as cursor:
        # Get all table names
        #cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            # Get all column details for the table
            #cursor.execute(f"PRAGMA table_info('{table_name}');")
            cursor.execute(f"SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = '{table_name}';")
            columns = cursor.fetchall()
            schema_data.append({
                'table_name': table_name,
                'columns': columns
            })

    return render(request, 'app/db_schema.html', {'schema_data': schema_data})

def product_list(request):
    products = product.objects.all().order_by('-product_id')[:200]  # Limit to the latest 200 products
    return render(request, 'app/product_list.html', {'products': products})

def generate_random_sku(length=10):
    """ Generate a random SKU """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_location():
    """ Generate a random location """
    locations = ['Warehouse A', 'Warehouse B', 'Warehouse C']  # Example locations
    return random.choice(locations)

def generate_random_product(request):
    """ View to generate random products """
    if request.method == 'POST':
        num_products = int(request.POST.get('num_products', 1))
        for _ in range(num_products):
            products = product(
                sku=generate_random_sku(),
                name=f"Product {random.randint(1, 100)}",
                description="Random description",
                price=random.uniform(10, 1000),  # Adjust as needed
                quantity=random.randint(0, 100),
                location=generate_random_location(),
            )
            products.save()
        #return redirect('generate_products_success', num_products=num_products)
        
    context = {'request': request}
            # Keep only the latest 200 products
    latest_200_ids = product.objects.all().order_by('-product_id').values_list('product_id', flat=True)[:200]
    product.objects.exclude(product_id__in=latest_200_ids).delete()
    products = product.objects.all().order_by('-product_id')  # Query all products from the database
    return render(request, 'app/generate_product.html',{'products': products})

def generate_product_success(request, num_products):
    """ Success page after generating products """
    return render(request, 'app/generate_product_success.html', {'num_products': num_products})

class ShowcaseView(View):
    
    def get(self, request):
        return render(request, 'app/showcase.html')

    def post(self, request):
        colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']
        random_color = random.choice(colors)
        
        return JsonResponse({'color': random_color})
    
def search_players(request):
    query = request.GET.get('q', '')
    results = SoccerPlayer.objects.filter(name__icontains=query) if query else []
    return render(request, 'app/search.html', {'query': query, 'results': results})

def data_page(request):
    # Load the dataset
    california_housing = fetch_california_housing()

    # Create a DataFrame from the dataset
    cal_data = pd.DataFrame(california_housing.data, columns=california_housing.feature_names)
    # Convert DataFrame to HTML
    html_table = cal_data.head(25).to_html(classes='table table-striped table-bordered', index=False)
    context = {
        'cal_housing' : html_table,
        'Correlation_Matrix_url':'/static/Correlation_Matrix.png',
        'Distribution_of_Median_House_Value_url':'/static/Distribution_of_Median_House_Value.png',
        'Feature_Importance_from_Random_Forest_url' : '/static/Feature_Importance_from_Random_Forest.png',
        #'coeffic_sorted_df_json_sorted':coeffic_sorted_df_json,
        #'Random_Forest_Mean_Squared_Error_txt' : Random_Forest_Mean_Squared_Error,
        #'Random_Forest_R2_Score_txt' : Random_Forest_R2_Score,
        #'featureimportance_txt' : featureimportance,
    }
    return render(request, 'app/data_page.html', context)

def sql(request):
    return render(request, 'app/sql.html')

def sql2(request):
    suppliers = Supplier.objects.all()
    products = Warehouse_Products.objects.all()
    customers = Customer.objects.all()
    orders = Order.objects.all()
    order_details = OrderDetail.objects.all()

    context = {
        'suppliers': suppliers,
        'products': products,
        'customers': customers,
        'orders': orders,
        'order_details': order_details,
    }
    return render(request, 'app/sql2.html', context)
