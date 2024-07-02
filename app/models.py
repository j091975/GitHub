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

    def __str__(self):
        return self.name