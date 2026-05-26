from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Processo, Magistrado, AtaDistribuicao
from .services import executar_distribuicao_regimental

def dashboard_distribuicao(request):
    processos_pendentes = Processo.objects.filter(status='CADASTRADO')
    total_juizes = Magistrado.objects.count()
    ultimas_atas = AtaDistribuicao.objects.all().order_by('-data_hora')[:5]


    if request.method == "POST" and 'rodar_sorteio' in request.POST:
        qtd_processados = executar_distribuicao_regimental()
        
        if qtd_processados > 0:
            messages.success(request, f'Sucesso! {qtd_processados} processos foram distribuídos conforme o Regimento.')
        else:
            messages.warning(request, 'Aviso: Fila vazia ou nenhum magistrado disponível para sorteio.')
            
        return redirect('dashboard')

    context = {
        'processos_pendentes': processos_pendentes,
        'total_juizes': total_juizes,
        'ultimas_atas': ultimas_atas,
    }
    return render(request, 'processos/dashboard.html', context)