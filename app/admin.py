from django.contrib import admin
from .models import SoccerPlayer, product

# Register the SoccerPlayer model
admin.site.register(SoccerPlayer)
admin.site.register(product)
