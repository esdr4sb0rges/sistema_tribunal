from django.db import models
from django.contrib.auth.models import User

class Magistrado(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        verbose_name="Usuário Sistema")
    
    #RF 06
    parentes = models.ManyToManyField(
        'self', blank=True, symmetrical=True,
        verbose_name="Parente")
    
    #RF 02 - 04
    saldo_processos = models.IntegerField(
        default=0, verbose_name="Conta de Distribuição")
    
    #RF 11
    genero = models.CharField(
        max_length=20, choices=[('M', 'Masculino'), ('F', 'Feminino')],
        null=True, blank=True
    )
    class Meta:
        verbose_name = "Magistrado"
        verbose_name_plural = "Magistrados"

    def __str__(self):
        return f"Mag. {self.user.get_full_name() or self.user.username} (Saldo: {self.saldo_processos})"
    
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