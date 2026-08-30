from decimal import Decimal
from django.shortcuts import render, redirect
from .models import ImportCalculation, Vehicle
from .services import calcular_landed_cost, analisar_oportunidade

def painel_calculadora(request):
    # 1. EDITAR CUSTOS DIRETO NA PAGINA 
    if request.method == 'POST' and 'update_costs' in request.POST:
        calculo_id = request.POST.get('calculo_id')
        calculo = ImportCalculation.objects.get(id=calculo_id)
        
        calculo.auction_fee = Decimal(request.POST.get('auction_fee', '0.00'))
        calculo.buyer_fees = Decimal(request.POST.get('buyer_fees', '0.00'))
        calculo.transport_cost = Decimal(request.POST.get('transport_cost', '0.00'))
        calculo.homologation_cost = Decimal(request.POST.get('homologation_cost', '0.00'))
        calculo.itv_cost = Decimal(request.POST.get('itv_cost', '0.00'))
        calculo.target_margin = Decimal(request.POST.get('target_margin', '0.00'))
        calculo.save()
        
        return redirect(f"/?carro_id={calculo.vehicle.id}")

    # 2. CRIAR NOVO VEICULO
    if request.method == 'POST' and 'create_vehicle' in request.POST:
        novo_veiculo = Vehicle.objects.create(
            make=request.POST.get('make'),
            model=request.POST.get('model'),
            version=request.POST.get('version', ''),
            transmission=request.POST.get('transmission', 'Automática'),
            seller=request.POST.get('seller', 'Particular'),
            year=int(request.POST.get('year')),
            mileage=int(request.POST.get('mileage')),
            purchase_price=Decimal(request.POST.get('purchase_price', '0.00')),
            currency=request.POST.get('currency', 'EUR'),
            market_type=request.POST.get('market_type'),
            origin_country=request.POST.get('origin_country', 'Espanha'),
            co2_emissions=int(request.POST.get('co2_emissions', 120)),
            fuel_type=request.POST.get('fuel_type', 'Gasolina'),
            source_url=request.POST.get('source_url', '')
        )

        if request.POST.get('market_type') == 'ORIGIN':
            ImportCalculation.objects.create(vehicle=novo_veiculo)

        return redirect('calculadora')

    # 3. CARREGAR VEICULO ATIVO
    veiculos_origem = Vehicle.objects.filter(market_type='ORIGIN')
    if not veiculos_origem.exists():
        return render(request, 'calculadora/calculator.html', {'todos_calculos': []})

    carro_id = request.GET.get('carro_id')
    veiculo_selecionado = veiculos_origem.filter(id=carro_id).first() if carro_id else veiculos_origem.first()
    if not veiculo_selecionado:
        veiculo_selecionado = veiculos_origem.first()

    calculo, _ = ImportCalculation.objects.get_or_create(vehicle=veiculo_selecionado)

    # 4. PROCESSAR RESULTADOS
    resumo_custos = calcular_landed_cost(calculo)
    resumo_oportunidade = analisar_oportunidade(veiculo_selecionado, resumo_custos)

    contexto = {
        'calculo': calculo,
        'veiculo': veiculo_selecionado,
        'custos': resumo_custos,
        'oportunidade': resumo_oportunidade,
        'todos_calculos': veiculos_origem,
    }

    return render(request, 'calculadora/calculator.html', contexto)