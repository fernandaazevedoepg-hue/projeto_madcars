import numpy as np
from decimal import Decimal
from .models import Vehicle

def calcular_landed_cost(calculo):
    veiculo = calculo.vehicle
    preco_base = veiculo.purchase_price

    # Subtotal Aquisicao e Logistica
    subtotal_aquisicao = preco_base + calculo.auction_fee + calculo.buyer_fees + calculo.documentation_cost
    subtotal_logistica = calculo.transport_cost

    # Imposto CO2 (IEDMT Espanha)
    co2 = veiculo.co2_emissions
    if co2 <= 120:
        taxa_iedmt = Decimal('0.00')
    elif co2 <= 160:
        taxa_iedmt = Decimal('0.0475')
    elif co2 <= 200:
        taxa_iedmt = Decimal('0.0975')
    else:
        taxa_iedmt = Decimal('0.1475')

    imposto_matricula = (preco_base * taxa_iedmt).quantize(Decimal('0.01'))

    # Subtotal Fiscal e Tramitacao
    subtotal_fiscal = calculo.homologation_cost + calculo.itv_cost + calculo.gestoria_cost + imposto_matricula

    # Landed Cost Total e Preco de Venda
    landed_cost = subtotal_aquisicao + subtotal_logistica + subtotal_fiscal
    preco_venda_sugerido = landed_cost + calculo.target_margin

    return {
        'preco_base': preco_base,
        'subtotal_aquisicao': subtotal_aquisicao,
        'subtotal_logistica': subtotal_logistica,
        'imposto_matricula': imposto_matricula,
        'subtotal_fiscal': subtotal_fiscal,
        'landed_cost': landed_cost,
        'target_margin': calculo.target_margin,
        'preco_venda_final': preco_venda_sugerido,
    }


def analisar_oportunidade(veiculo_origem, resumo_custos):
    # Comparaveis em Espanha 
    comparaveis = Vehicle.objects.filter(
        market_type='SPAIN',
        make__iexact=veiculo_origem.make,
        model__icontains=veiculo_origem.model.split()[0],
        year__gte=veiculo_origem.year - 3,
        year__lte=veiculo_origem.year + 3,
        fuel_type=veiculo_origem.fuel_type,
        transmission=veiculo_origem.transmission
    )

    total_comp = comparaveis.count()

    if total_comp > 0:
        precos = [float(c.purchase_price) for c in comparaveis]
        preco_min = Decimal(str(np.min(precos))).quantize(Decimal('0.01'))
        preco_max = Decimal(str(np.max(precos))).quantize(Decimal('0.01'))
        preco_medio = Decimal(str(np.mean(precos))).quantize(Decimal('0.01'))
        preco_mediana = Decimal(str(np.median(precos))).quantize(Decimal('0.01'))
    else:
        preco_min = preco_max = preco_medio = preco_mediana = Decimal('0.00')

    landed_cost = resumo_custos['landed_cost']
    preco_venda_final = resumo_custos['preco_venda_final']

    margem_eur = preco_medio - landed_cost
    margem_pct = (margem_eur / landed_cost * Decimal('100')).quantize(Decimal('0.01')) if landed_cost > 0 else Decimal('0.00')
    poupanca_cliente = preco_medio - preco_venda_final

    # Algoritmo de Score
    score_margem = 60 if margem_pct >= 20 else (40 if margem_pct >= 10 else (20 if margem_pct > 0 else 0))
    score_amostra = 40 if total_comp >= 5 else (25 if total_comp >= 2 else (10 if total_comp == 1 else 0))
    total_score = score_margem + score_amostra

    if total_score >= 80:
        status = 'Good Opportunity'
        status_cor = 'success'
    elif total_score >= 60:
        status = 'Review Required'
        status_cor = 'warning'
    else:
        status = 'Not Attractive'
        status_cor = 'danger'

    return {
        'total_comparaveis': total_comp,
        'preco_min': preco_min,
        'preco_max': preco_max,
        'preco_medio': preco_medio,
        'preco_mediana': preco_mediana,
        'margem_eur': margem_eur,
        'margem_pct': margem_pct,
        'poupanca_cliente': poupanca_cliente,
        'score': total_score,
        'status': status,
        'status_cor': status_cor,
        'lista_comparaveis': comparaveis
    }