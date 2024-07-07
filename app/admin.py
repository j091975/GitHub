from django.contrib import admin
from .models import SoccerPlayer, product, Slide

# Register the SoccerPlayer model
admin.site.register(SoccerPlayer)
admin.site.register(product)
admin.site.register(Slide)