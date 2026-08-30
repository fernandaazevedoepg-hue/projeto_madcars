from decimal import Decimal
from django.db import models

class Vehicle(models.Model):
    MARKET_CHOICES = [
        ('SPAIN', 'Comparável (Espanha)'),
        ('ORIGIN', 'Carro p/ Importar (Origem)'),
    ]

    TRANSMISSION_CHOICES = [
        ('Automática', 'Automática'),
        ('Manual', 'Manual'),
    ]

    FUEL_CHOICES = [
        ('Gasolina', 'Gasolina'),
        ('Diesel', 'Diesel'),
        ('Híbrido', 'Híbrido'),
        ('Elétrico', 'Elétrico'),
    ]

    make = models.CharField(max_length=100, verbose_name="Marca")
    model = models.CharField(max_length=100, verbose_name="Modelo")
    version = models.CharField(max_length=100, blank=True, default='', verbose_name="Versão")
    year = models.IntegerField(verbose_name="Ano")
    mileage = models.IntegerField(verbose_name="Quilometragem (km)")
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Preço de Compra")
    currency = models.CharField(max_length=10, default='EUR', verbose_name="Moeda")
    origin_country = models.CharField(max_length=100, default='Espanha', verbose_name="País de Origem")
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='Automática', verbose_name="Transmissão")
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='Gasolina', verbose_name="Combustível")
    co2_emissions = models.IntegerField(default=120, verbose_name="Emissões CO₂ (g/km)")
    engine_size = models.CharField(max_length=50, blank=True, default='', verbose_name="Cilindrada")
    power = models.CharField(max_length=50, blank=True, default='', verbose_name="Potência (cv)")
    market_type = models.CharField(max_length=10, choices=MARKET_CHOICES, default='SPAIN', verbose_name="Tipo de Mercado")
    seller = models.CharField(max_length=255, blank=True, default='Particular', verbose_name="Vendedor")
    source_url = models.URLField(blank=True, default='', verbose_name="URL do Anúncio")

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"

    def __str__(self):
        return f"{self.make} {self.model} ({self.year}) - {self.purchase_price} {self.currency}"


class ImportCalculation(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name='import_calculation', verbose_name="Veículo")
    
    # Custos Principais da Importacao
    auction_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('485.00'), verbose_name="Taxa de Leilão (€)")
    buyer_fees = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('430.00'), verbose_name="Honorários Comprador (€)")
    documentation_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('90.00'), verbose_name="Custo Documentação (€)")
    transport_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('826.00'), verbose_name="Custo Transporte (€)")
    homologation_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('60.00'), verbose_name="Custo Homologação (€)")
    itv_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('141.32'), verbose_name="Custo ITV (€)")
    gestoria_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('150.00'), verbose_name="Custo Gestoria (€)")
    
    # Margem Comercial Pretendida
    target_margin = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('2000.00'), verbose_name="Margem Alvo (€)")

    class Meta:
        verbose_name = "Cálculo de Importação"
        verbose_name_plural = "Cálculos de Importação"

    def __str__(self):
        return f"Cálculo - {self.vehicle}"