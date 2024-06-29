from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import date, datetime

class product(models.Model):
    product_id = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    location = models.TextField()
    DateAdded = models.DateField(default=datetime.now)
    DateUpdated = models.DateField(default=datetime.now)
    
    class Meta:
        db_table = 'store_product'  # Explicitly specify the table name
        
    def __str__(self):
        return self.name