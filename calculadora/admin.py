from django.contrib import admin
from .models import Vehicle, ImportCalculation

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'seller', 'purchase_price', 'market_type', 'origin_country')
    list_filter = ('market_type', 'make', 'origin_country')
    search_fields = ('make', 'model')

@admin.register(ImportCalculation)
class ImportCalculationAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'transport_cost', 'target_margin')