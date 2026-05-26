from processos.models import Processo, Magistrado, EstadoExclusao, AtaDistribuicao
from django.utils import timezone

def executar_distribuicao_regimental():
    hoje = timezone.now().date()
    processos_na_fila = Processo.objects.filter(status='CADASTRADO')
    
    magistrados_excluidos_ids = EstadoExclusao.objects.filter(
        data_inicio__lte=hoje,
        data_fim__gte=hoje
    ).values_list('magistrado_id', flat=True)

    juizes_elegiveis = Magistrado.objects.exclude(id__in=magistrados_excluidos_ids)

    if not processos_na_fila.exists() or not juizes_elegiveis.exists():
        return 0  

    contador_sucesso = 0

    for processo in processos_na_fila:
        if processo.processo_prevento and processo.processo_prevento.relator:
            juiz_sorteado = processo.processo_prevento.relator
            tipo_dist = "Ata de Distribuição"
            fundamento = "Art. 26, §1º e §2º."
        else:
            juiz_sorteado = None
            for juiz in juizes_elegiveis.order_by('saldo_processos'):
                if processo.processo_prevento and processo.processo_prevento.relator:
                    relator_antigo = processo.processo_prevento.relator
                    if juiz.parente == relator_antigo or relator_antigo.parente == juiz:
                        continue  

                juiz_sorteado = juiz
                break

            if not juiz_sorteado:
                juiz_sorteado = juizes_elegiveis.order_by('saldo_processos').first()

            tipo_dist = "Sorteio Automatizado por Menor Carga"
            fundamento = "Art. 25, §4º."

        processo.relator = juiz_sorteado
        processo.status = 'DISTRIBUIDO'
        processo.save()

        juiz_sorteado.saldo_processos += 1
        juiz_sorteado.save()

        AtaDistribuicao.objects.create(
            processo_numero=processo.numero,
            classe_sigla=processo.classe_processual.sigla,
            magistrado_sorteado=juiz_sorteado.user.get_full_name() or juiz_sorteado.user.username,
            tipo_distribuicao=tipo_dist,
            fundamento_legal=fundamento
        )
        contador_sucesso += 1

    return contador_sucesso