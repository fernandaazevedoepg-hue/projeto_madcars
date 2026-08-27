from django.contrib import admin
from .models import Vehicle, ImportCalculation

# Registar os modelos no painel de administração
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    list_display = ('make', 'model', 'year', 'purchase_price', 'market_type', 'origin_country')
    list_filter = ('market_type', 'make', 'fuel_type')
    search_fields = ('make', 'model')

@admin.register(ImportCalculation)
class ImportCalculationAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'transport_cost', 'auction_fee', 'target_margin')