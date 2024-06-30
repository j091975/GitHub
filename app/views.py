from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from .models import product, SoccerPlayer
from .forms import ProductForm  # Assuming you have a form for the Product
import random
import string
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


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

def wiki(request):
    return render(request, 'app/wiki.html')

def links(request):
    return render(request, 'app/links.html')

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
    products = product.objects.all()  # Query all products from the database
    return render(request, 'app/product_list.html', {'products': products})

def generate_random_sku(length=10):
    """ Generate a random SKU """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

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
        return redirect('generate_products_success', num_products=num_products)
    return render(request, 'app/generate_product.html')

def generate_product_success(request, num_products):
    """ Success page after generating products """
    return render(request, 'app/generate_product_success.html', {'num_products': num_products})

class ShowcaseView(View):
    
    def get(self, request):
        return render(request, 'app/showcase.html')

    @method_decorator(csrf_exempt)  # Only for demonstration, not secure in production
    def post(self, request):
        colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']
        random_color = random.choice(colors)
        #print(random_color)
        return JsonResponse({'color': random_color})
    
def search_players(request):
    query = request.GET.get('q', '')
    results = SoccerPlayer.objects.filter(name__icontains=query) if query else []
    return render(request, 'app/search.html', {'query': query, 'results': results})