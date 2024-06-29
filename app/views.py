from django.shortcuts import render, redirect
from django.db import connection
from .models import product
from .forms import ProductForm  # Assuming you have a form for the Product

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