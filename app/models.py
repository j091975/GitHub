from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import date, datetime
import random
import string

class product(models.Model):
    product_id = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    location = models.TextField()
    dateadded = models.DateField(default=datetime.now)
    dateupdated = models.DateField(default=datetime.now)
    
    class Meta:
        db_table = 'store_product'  # Explicitly specify the table name
        
    def __str__(self):
        return self.name
    
class SoccerPlayer(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    club = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)

    class Meta:
        db_table = 'SoccerPlayer'  # Explicitly specify the table name
        
    def __str__(self):
        return self.name    
    
class Slide(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='carousel_images/')

    class Meta:
        db_table = 'Slide'
        
    def __str__(self):
        return self.title

    

class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    class Meta:
        db_table = 'Supplier'  # Explicitly specify the table name 


class Warehouse_Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, blank=True, null=True)
    quantity_per_unit = models.CharField(max_length=100, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    units_in_stock = models.IntegerField(blank=True, null=True)
    units_on_order = models.IntegerField(blank=True, null=True)
    reorder_level = models.IntegerField(blank=True, null=True)
    discontinued = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name 


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.customer_name
    
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField(blank=True, null=True)
    required_date = models.DateField(blank=True, null=True)
    shipped_date = models.DateField(blank=True, null=True)
    ship_via = models.CharField(max_length=100, blank=True, null=True)
    freight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ship_name = models.CharField(max_length=255, blank=True, null=True)
    ship_address = models.CharField(max_length=255, blank=True, null=True)
    ship_city = models.CharField(max_length=100, blank=True, null=True)
    ship_postal_code = models.CharField(max_length=50, blank=True, null=True)
    ship_country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Order {self.order_id} for {self.customer.customer_name}"
    
class OrderDetail(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Warehouse_Products, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Order Detail {self.order_detail_id} for Order {self.order.order_id}"


# Sample data generation functions
#def random_string(length=10):
#    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
#
#def random_bool(length=10):
#    return random.randint(0, 1)
#
#def random_int_id(length=10):
#    return random.randint(1, 1000)
#
#def random_int(min_value, max_value):
#    return random.randint(min_value, max_value)
#
#from decimal import Decimal
#
#def random_decimal(min_value, max_value, precision=2):
#    # Generate a random float between min_value and max_value
#    random_float = random.uniform(min_value, max_value)
#    
#    # Convert to Decimal with specified precision
#    return Decimal(random_float).quantize(Decimal(10) ** -precision)
#
#def random_phone():
#    return ''.join(random.choice(string.digits) for _ in range(10))
#
#def random_date():
#    year = random.randint(2020, 2023)
#    month = random.randint(1, 12)
#    day = random.randint(1, 28)
#    return f"{year}-{month:02d}-{day:02d}"
#
#def generate_random_postal_code():
#    # Define the format: 2 uppercase letters + 2 digits + 1 space + 1 uppercase letter + 1 uppercase letter
#    letters = string.ascii_uppercase
#    digits = string.digits
#
#    postal_code = (
#        random.choice(letters) +
#        random.choice(letters) +
#        random.choice(digits) +
#        random.choice(digits) +
#        ' ' +
#        random.choice(letters) +
#        random.choice(letters)
#    )
#    return postal_code
#
#from django.db import transaction
#
## Generate sample data
#sample_data = [
#    {
#        'supplier_name': random_string(),
#        'contact_name': random_string(),
#        'phone': random_phone(),
#        'address': random_string(),
#        'city': random_string(),
#        'postal_code': generate_random_postal_code(),
#        'country': random_string()
#    }
#    for _ in range(20)  # Generate 20 sample entries
#]
#
#try:
#    # Bulk insert the sample data into the database using a transaction for efficiency
#    with transaction.atomic():
#        Supplier.objects.bulk_create([Supplier(**data) for data in sample_data])
#except:
#    None
# 
## Fetch all supplier IDs from the Supplier table
#supplier_ids = list(Supplier.objects.values_list('supplier_id', flat=True))
#    
#sample_data = [
#    {
#    'product_name': random_string(),
#    'supplier_id': random.choice(supplier_ids),
#    'category': random_string(),
#    'quantity_per_unit': random_int(1,10),
#    'unit_price': random_decimal(0, 100, precision=2),
#    'units_in_stock': random_int(3,100),
#    'units_on_order': random_int(0,33),
#    'reorder_level': random_int(20,50),
#    'discontinued': random_bool()
#    }
#    for _ in range(20)  # Generate 20 sample entries     
#]
#
#try:
#    # Bulk insert the sample data into the database using a transaction for efficiency
#    with transaction.atomic():
#        Warehouse_Products.objects.bulk_create([Warehouse_Products(**data) for data in sample_data])
#except Exception as e:
#    print('Products insert failed:', str(e))
#    
#    
#sample_data = [
#    {
#    'customer_name': random_string(),
#    'contact_name': random_string(),
#    'phone': random_phone(),
#    'address': random_string(),
#    'city': random_string(),
#    'postal_code': generate_random_postal_code(),
#    'country': random_string()
#    }
#    for _ in range(20)  # Generate 20 sample entries     
#]
#
#try:
#    # Bulk insert the sample data into the database using a transaction for efficiency
#    with transaction.atomic():
#        Customer.objects.bulk_create([Customer(**data) for data in sample_data])
#except Exception as e:
#    print('Customer insert failed:', str(e))
#    
#
#customer_ids = list(Customer.objects.values_list('customer_id', flat=True))
#sample_data = [
#    {
#    'customer_id': random.choice(customer_ids),
#    'order_date': random_date(),
#    'required_date': random_date(),
#    'shipped_date': random_date(),
#    'ship_via': random_string(),
#    'freight': random_decimal(0, 100, precision=2),
#    'ship_name': random_string(),
#    'ship_address': random_string(),
#    'ship_city': random_string(),
#    'ship_postal_code': generate_random_postal_code(),
#    'ship_country': random_string()
#    }
#    for _ in range(20)  # Generate 20 sample entries
#]
#
#try:
#    # Bulk insert the sample data into the database using a transaction for efficiency
#    with transaction.atomic():
#        Order.objects.bulk_create([Order(**data) for data in sample_data])
#except Exception as e:
#    print('Order insert failed:', str(e))
#
#order_ids = list(Order.objects.values_list('order_id', flat=True))
#product_ids = list(Warehouse_Products.objects.values_list('product_id', flat=True))    
#sample_data = [
#    {
#    'order_id': random.choice(order_ids),
#    'product_id': random.choice(product_ids),
#    'unit_price': random_decimal(0, 100, precision=2),
#    'quantity': random_int(1,45),
#    'discount': random_decimal(0, 100, precision=2)
#    }
#    for _ in range(20)  # Generate 20 sample entries     
#]
#
#try:
#    # Bulk insert the sample data into the database using a transaction for efficiency
#    with transaction.atomic():
#        OrderDetail.objects.bulk_create([OrderDetail(**data) for data in sample_data])
#except Exception as e:
#    print('OrderDetail insert failed:', str(e))