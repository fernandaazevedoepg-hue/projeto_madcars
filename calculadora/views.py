from django.shortcuts import render, redirect
from .models import ImportCalculation, Vehicle
from .services import calcular_landed_cost, analisar_oportunidade

def painel_calculadora(request):
    # 1. PROCESSAR FORMULÁRIO (Criação de novos veículos)
    if request.method == 'POST':
        make = request.POST.get('make')
        model = request.POST.get('model')
        version = request.POST.get('version', '')
        seller = request.POST.get('seller', 'Particular')
        year = int(request.POST.get('year'))
        mileage = int(request.POST.get('mileage'))
        purchase_price = float(request.POST.get('purchase_price'))
        market_type = request.POST.get('market_type')
        origin_country = request.POST.get('origin_country', 'Espanha')
        co2_emissions = int(request.POST.get('co2_emissions', 120))
        fuel_type = request.POST.get('fuel_type', 'Gasolina')

        novo_veiculo = Vehicle.objects.create(
            make=make,
            model=model,
            version=version,
            year=year,
            mileage=mileage,
            purchase_price=purchase_price,
            market_type=market_type,
            origin_country=origin_country,
            co2_emissions=co2_emissions,
            seller=seller,
            fuel_type=fuel_type
        )

        if market_type == 'ORIGIN':
            ImportCalculation.objects.create(
                vehicle=novo_veiculo,
                auction_fee=485.00,
                buyer_fees=430.00,
                transport_cost=826.00,
                homologation_cost=60.00,
                itv_cost=141.32,
                target_margin=2000.00
            )

        return redirect('calculadora')

    # 2. CARREGAR O CÁLCULO SELECIONADO OU O MAIS RECENTE
    carro_id = request.GET.get('carro_id')
    
    if carro_id:
        calculo = ImportCalculation.objects.filter(id=carro_id).first()
    else:
        calculo = ImportCalculation.objects.last()

    if not calculo:
        return render(request, 'calculadora/vazio.html')

    resumo_custos = calcular_landed_cost(calculo)
    resumo_oportunidade = analisar_oportunidade(calculo.vehicle, resumo_custos)
    todos_calculos = ImportCalculation.objects.all()

    contexto = {
        'calculo': calculo,
        'veiculo': calculo.vehicle,
        'custos': resumo_custos,
        'oportunidade': resumo_oportunidade,
        'todos_calculos': todos_calculos,
    }

    return render(request, 'calculadora/calculator.html', contexto)