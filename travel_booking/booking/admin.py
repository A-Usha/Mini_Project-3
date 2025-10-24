from django.contrib import admin
from .models import TravelSystem

@admin.register(TravelSystem)
class TravelSystemAdmin(admin.ModelAdmin):
    list_display = ('mode', 'source', 'destination', 'price', 'available_seats')
