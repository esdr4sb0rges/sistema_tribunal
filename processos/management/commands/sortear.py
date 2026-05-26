from django.core.management.base import BaseCommand
from processos.models import Processo, EstadoExclusao, Magistrado, AtaDistribuicao
from django.contrib.auth.models import User
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Motor de Sorteio'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING(f'[{timezone.now()}] Iniciando Kernel de Sorteio Avançado...'))

        processos_na_fila = Processo.objects.filter(status='CADASTRADO')
        hoje = timezone.now() .date()

        magistrados_excluidos_ids = EstadoExclusao.objects.filter(
            data_inicio__lte=hoje,
            data_fim__gte=hoje
        )  .values_list ('magistrado_id', flat=True)

        juizes_elegiveis = Magistrado.objects.exclude(id__in=magistrados_excluidos_ids) 

        if not processos_na_fila.exists() or not juizes_elegiveis.exists():
            self.stdout.write(self.style.SUCCESS('Sem processos na fila ou sem juízes cadastrados.'))
            return

        for processo in processos_na_fila:
            # REGRA 1: CASO REABERTO (Devolução)
            if processo.processo_prevento and processo.processo_prevento.relator:
                juiz_sorteado = processo.processo_prevento.relator
                self.stdout.write(self.style.WARNING(f' Prevento -> Vinculado ao Relator original: {juiz_sorteado.user.username}'))

            else:
                juiz_sorteado = juizes_elegiveis.order_by('saldo_processos').first()
                self.stdout.write(self.style.SUCCESS(f'Sorteio -> Selecionado por menor carga: {juiz_sorteado.user.username}'))

            processo.relator = juiz_sorteado
            processo.status = 'DISTRIBUIDO'
            processo.save()

            juiz_sorteado.saldo_processos += 1
            juiz_sorteado.save()

            #Criar a Ata
            if processo.processo_prevento and processo.processo_prevento.relator:
                tipo_dist = "Ata de Distribuição"
                fundamento = "Art. 26, §1º e §2º."
            else:
                tipo_dist = "Sorteio Automatizado por Menor Carga"
                fundamento = "Art. 25, §4º ."

            AtaDistribuicao.objects.create(
                processo_numero=processo.numero,
                classe_sigla=processo.classe_processual.sigla,
                magistrado_sorteado=juiz_sorteado.user.get_full_name() or juiz_sorteado.user.username,
                tipo_distribuicao=tipo_dist,
                fundamento_legal=fundamento
            )
            self.stdout.write(self.style.SUCCESS(f'📜 Ata de auditoria gerada para o Processo {processo.numero}'))

        self.stdout.write(self.style.WARNING('========================================='))
        self.stdout.write(self.style.SUCCESS('Sorteio finalizado. Painel atualizado.'))