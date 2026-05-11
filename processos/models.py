from django.db import models
from django.contrib.auth.models import User

class Processo(models.Model):
    NIVEL_CHOICES = [
        ('BASICO', 'Básico (Geralmente CPF)'),
        ('INTERMEDIÁRIO', 'Intermediário (Geralmente CPF)'),
        ('COMPLEXO', 'Complexo (Geralmente CNPJ)'),
    ]

    STATUS_CHOICES = [
        ('CADASTRADO', 'Cadastrado (Aguardando Sorteio)'),
        ('DISTRIBUIDO', 'Distribuido (Sorteado)'),
        ('CONFIRMADO', 'Aguardando Forasteiro (Conflito de Interesse)'),
    ]

    numero = models.CharField(max_length=50, unique=True, verbose_name="Número do Processo")
    documento = models.CharField(max_length=20, verbose_name="CPF/CNPJ")
    nivel = models.CharField(max_length=15, choices=NIVEL_CHOICES, verbose_name="Nível de Complexidade")
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='CADASTRADO', verbose_name="Status")
    reaberto = models.BooleanField(default=False, verbose_name="É um caso reaberto?")
    data_cadastro = models.DateTimeField(auto_now_add=True)

    juiz_responsavel = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="Juiz Responsável"
    )

    class Meta:
        verbose_name = "Processo"
        verbose_name_plural = "Processos"

    def __str__(self):
        return f"{self.numero} - {self.get_nivel_display()}"
    
class ConflitoInteresse(models.Model):
    processo = models.ForeignKey(
    Processo, on_delete=models.CASCADE,
        verbose_name="Processo com Conflito"
    )
    juiz = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name="Juiz declarou Conflito"
    )
    justificativa = models.TextField(verbose_name="Justificativa de Conflito")
    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Conflito de Interesse"
        verbose_name_plural = "Conflitos de Interesse"

    def __str__(self):
        return f"Conflito: Processo {self.processo.numero} - Juiz ID: {self.juiz.id}"