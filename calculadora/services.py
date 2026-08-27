from decimal import Decimal
import numpy as np
from .models import Vehicle

def calcular_imposto_matriculacao(preco_compra, co2):

    preco = Decimal(str(preco_compra))
    
    if co2 <= 120:
        taxa = Decimal('0.00')
    elif 120 < co2 <= 160:
        taxa = Decimal('0.0475')
    elif 160 < co2 <= 200:
        taxa = Decimal('0.0975')
    else:
        taxa = Decimal('0.1475')

    return preco * taxa


def calcular_landed_cost(calculo_obj):
    veiculo = calculo_obj.vehicle
    preco_base = veiculo.purchase_price
    
    #Custos de Aquisição
    subtotal_aquisicao = preco_base + calculo_obj.auction_fee + calculo_obj.buyer_fees
    
    #Custos Logísticos
    subtotal_logistica = calculo_obj.transport_cost
    
    #Imposto de Matriculação Automático
    imposto_matricula = calcular_imposto_matriculacao(preco_base, veiculo.co2_emissions)
    
    #Custos Legais e Fiscais
    subtotal_fiscal = calculo_obj.homologation_cost + calculo_obj.itv_cost + imposto_matricula
    
    #Landed Cost = Aquisição + Logística + Fiscal
    landed_cost = subtotal_aquisicao + subtotal_logistica + subtotal_fiscal
    preco_venda_final = landed_cost + calculo_obj.target_margin

    return {
        'subtotal_aquisicao': round(subtotal_aquisicao, 2),
        'subtotal_logistica': round(subtotal_logistica, 2),
        'imposto_matricula': round(imposto_matricula, 2),
        'subtotal_fiscal': round(subtotal_fiscal, 2),
        'landed_cost': round(landed_cost, 2),
        'preco_venda_final': round(preco_venda_final, 2)
    }


def analisar_oportunidade(veiculo_origem, resumo_custos):
    modelo_base = veiculo_origem.model.split()[0]

    comparaveis = Vehicle.objects.filter(
        make__icontains=veiculo_origem.make,
        model__icontains=modelo_base,
        year__gte=veiculo_origem.year - 3,
        year__lte=veiculo_origem.year + 3
    ).exclude(id=veiculo_origem.id)

    precos = [float(c.purchase_price) for c in comparaveis]
    landed_cost = float(resumo_custos['landed_cost'])
    preco_venda_proposito = float(resumo_custos['preco_venda_final'])

    if not precos:
        return {
            'total_comparaveis': 0,
            'preco_medio': 0, 'preco_minimo': 0, 'preco_maximo': 0, 'mediana': 0,
            'margem_eur': 0, 'margem_pct': 0, 'score': 0,
            'status': 'Not Attractive', 'status_cor': 'danger',
            'motivo': 'Sem dados de veículos comparáveis em Espanha'
        }

    preco_medio = float(np.mean(precos))
    preco_minimo = float(np.min(precos))
    preco_maximo = float(np.max(precos))
    mediana = float(np.median(precos))

    margem_eur = preco_medio - landed_cost
    margem_pct = (margem_eur / landed_cost) * 100 if landed_cost > 0 else 0

    if margem_pct >= 20:
        pts_margem = 60
    elif margem_pct >= 10:
        pts_margem = 40
    elif margem_pct > 0:
        pts_margem = 20
    else:
        pts_margem = 0

    qtd_amostra = len(precos)
    if qtd_amostra >= 5:
        pts_amostra = 40
    elif qtd_amostra >= 2:
        pts_amostra = 25
    else:
        pts_amostra = 10

    total_score = pts_margem + pts_amostra

    if total_score >= 80:
        status = 'Good Opportunity'
        status_cor = 'success'  
    elif total_score >= 50:
        status = 'Review Required'
        status_cor = 'warning'  
    else:
        status = 'Not Attractive'
        status_cor = 'danger'   

    return {
        'total_comparaveis': qtd_amostra,
        'preco_medio': round(preco_medio, 2),
        'preco_minimo': round(preco_minimo, 2),
        'preco_maximo': round(preco_maximo, 2),
        'mediana': round(mediana, 2),
        'margem_eur': round(margem_eur, 2),
        'margem_pct': round(margem_pct, 2),
        'poupanca_cliente': round(preco_medio - preco_venda_proposito, 2),
        'score': total_score,
        'status': status,
        'status_cor': status_cor,
        'lista_comparaveis': comparaveis
    }