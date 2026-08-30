from django.contrib import admin
from .models import Vehicle, ImportCalculation

@admin.action(description="Duplicar veículos selecionados")
def duplicar_veiculos(modeladmin, request, queryset):
    for veiculo in queryset:
        veiculo.pk = None  
        veiculo.id = None  
        veiculo.save()


class ImportCalculationInline(admin.StackedInline):
    model = ImportCalculation
    can_delete = False
    verbose_name_plural = 'Cálculo de Importação'

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'make', 
        'model', 
        'version', 
        'market_type', 
        'transmission', 
        'fuel_type', 
        'year', 
        'purchase_price', 
        'origin_country'
    )
 
    list_filter = ('market_type', 'make', 'transmission', 'fuel_type', 'year')

    search_fields = ('make', 'model', 'version', 'seller')

    actions = [duplicar_veiculos]

    inlines = [ImportCalculationInline]

    fieldsets = (
        ('Informação Principal', {
            'fields': ('market_type', 'make', 'model', 'version')
        }),
        ('Especificações Técnicas', {
            'fields': ('transmission', 'fuel_type', 'co2_emissions', 'year', 'mileage')
        }),
        ('Valores e Origem', {
            'fields': ('purchase_price', 'origin_country', 'seller')
        }),
    )

@admin.register(ImportCalculation)
class ImportCalculationAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'transport_cost', 'itv_cost', 'target_margin')