from django.contrib import admin
from .models import SoccerPlayer, product, Slide, Supplier, Order, OrderDetail, Customer, Warehouse_Products

# Register the SoccerPlayer model
admin.site.register(SoccerPlayer)
admin.site.register(product)
admin.site.register(Slide)
admin.site.register(Supplier)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Customer)
admin.site.register(Warehouse_Products)