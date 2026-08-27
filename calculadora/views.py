from django.shortcuts import render
from .models import ImportCalculation
from .services import calcular_landed_cost, analisar_oportunidade

def painel_calculadora(request):
    #Procura o cálculo de importação associado ao veículo de origem
    calculo = ImportCalculation.objects.first()

    if not calculo:
        return render(request, 'calculadora/vazio.html')

    # Executa o motor financeiro para calcular o Landed Cost
    resumo_custos = calcular_landed_cost(calculo)

    #Executa o motor de mercado e gera o Opportunity Score
    resumo_oportunidade = analisar_oportunidade(calculo.vehicle, resumo_custos)

    #Organiza os dados para entregar ao HTML
    contexto = {
        'calculo': calculo,
        'veiculo': calculo.vehicle,
        'custos': resumo_custos,
        'oportunidade': resumo_oportunidade,
    }

    return render(request, 'calculadora/calculator.html', contexto)