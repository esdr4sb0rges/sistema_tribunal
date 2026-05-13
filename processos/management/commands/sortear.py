from django.core.management.base import BaseCommand
from processos.models import Processo
from django.contrib.auth.models import User
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Motor de Sorteio'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING(f'[{timezone.now()}] Iniciando Kernel de Sorteio Avançado...'))

        processos_na_fila = Processo.objects.filter(status='CADASTRADO')
        juizes = list(User.objects.all())

        if not processos_na_fila.exists() or not juizes:
            self.stdout.write(self.style.SUCCESS('Sem processos na fila ou sem juízes cadastrados.'))
            return

        for processo in processos_na_fila:
            # REGRA 1: CASO REABERTO (Devolução)
            if processo.reaberto and processo.juiz_responsavel:
                self.stdout.write(self.style.WARNING(f'{processo.numero} (REABERTO) -> Devolvido para: {processo.juiz_responsavel.username}'))
                processo.status = 'DISTRIBUIDO'
                processo.save()
                continue

            # REGRA 2: CASO NÍVEL COMPLEXO
            if processo.nivel == 'COMPLEXO':
                # O sistema calcula em tempo real quem tem menos casos complexos
                contagem_complexos = {
                    juiz: Processo.objects.filter(juiz_responsavel=juiz, nivel='COMPLEXO').count() 
                    for juiz in juizes
                }
                juiz_sorteado = min(contagem_complexos, key=contagem_complexos.get)
                
                self.stdout.write(self.style.ERROR(f'{processo.numero} (COMPLEXO) -> Sorteado para: {juiz_sorteado.username}'))

            # REGRA 3: CASO BÁSICOS E INTERMEDIÁRIOS
            else:
                juiz_sorteado = random.choice(juizes)
                self.stdout.write(self.style.SUCCESS(f' {processo.numero} ({processo.nivel}) -> Sorteado para: {juiz_sorteado.username}'))

            processo.juiz_responsavel = juiz_sorteado
            processo.status = 'DISTRIBUIDO'
            processo.save()

        self.stdout.write(self.style.WARNING('========================================='))
        self.stdout.write(self.style.SUCCESS('Sorteio finalizado. Painel atualizado.'))