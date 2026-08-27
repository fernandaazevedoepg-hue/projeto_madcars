from django.db import models

class Vehicle(models.Model):
   
    MARKET_CHOICES = [
        ('ORIGIN', 'Mercado de Origem (Alemanha, EAU, etc.)'),
        ('SPAIN', 'Mercado de Destino (Espanha)'),
    ]
    make = models.CharField(max_length=50, verbose_name="Marca")
    model = models.CharField(max_length=50, verbose_name="Modelo")
    version = models.CharField(max_length=100, blank=True, null=True, verbose_name="Versão")
    year = models.IntegerField(verbose_name="Ano")
    mileage = models.IntegerField(verbose_name="Quilometragem (km)")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Base (€)")
    origin_country = models.CharField(max_length=50, verbose_name="País de Origem")
    fuel_type = models.CharField(max_length=30, verbose_name="Combustível")
    co2_emissions = models.IntegerField(default=150, verbose_name="Emissões CO2 (g/km)")
    market_type = models.CharField(max_length=10, choices=MARKET_CHOICES, default='ORIGIN')
    source_url = models.URLField(blank=True, null=True, verbose_name="URL do Anúncio")

    def __str__(self):
        return f"{self.make} {self.model} ({self.year}) - {self.purchase_price}€"


class ImportCalculation(models.Model):
   
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name="calculation")
    
    auction_fee = models.DecimalField(max_digits=8, decimal_places=2, default=485.00, verbose_name="Taxa de Leilão (€)")
    buyer_fees = models.DecimalField(max_digits=8, decimal_places=2, default=430.00, verbose_name="Honorários (€)")
    transport_cost = models.DecimalField(max_digits=8, decimal_places=2, default=826.00, verbose_name="Transporte (€)")
    homologation_cost = models.DecimalField(max_digits=8, decimal_places=2, default=60.00, verbose_name="Ficha Reduzida (€)")
    itv_cost = models.DecimalField(max_digits=8, decimal_places=2, default=141.32, verbose_name="ITV (€)")
    target_margin = models.DecimalField(max_digits=8, decimal_places=2, default=2000.00, verbose_name="Margem Madcars (€)")

    def __str__(self):
        return f"Calculadora - {self.vehicle.make} {self.vehicle.model}"
