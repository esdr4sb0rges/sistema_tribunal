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
class ClasseProcessual(models.Model):
    ORGAO_CHOICES = [
        ('PLENO', 'Tribunal Pleno (26)'),
        ('TURMAS', 'Turmas (14)'),
        ('PRESIDENCIA', 'Presidência (2)'),
    ]
    nome = models.CharField(max_length=150, verbose_name="Nome da Classe")
    sigla = models.CharField(max_length=20, verbose_name="Sigla")
    orgao_competente = models.CharField(max_length=20, choices=ORGAO_CHOICES, verbose_name="Órgão Competente")

    # Atende a exigência: "O sistema precisa suportar versionamento"
    ativo = models.BooleanField(default=True, verbose_name="Classe Ativa/Vigente?")
    data_criacao = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Classe Processual"
        verbose_name_plural = "Classes Processuais"
        
    def __str__(self):
        return f"{self.sigla} - {self.nome} ({self.get_orgao_competente_display()})"

class Processo(models.Model):
    STATUS_CHOICES = [
        ('CADASTRADO', 'Cadastrado (Aguardando Distribuição)'),
        ('DISTRIBUIDO', 'Distribuído'),
        ('SUSPENSO', 'Suspenso / Excluído da Distribuição'),
    ]
    numero = models.CharField(max_length=50, unique=True, verbose_name="Número do Processo")
    classe_processual = models.ForeignKey(ClasseProcessual, on_delete=models.RESTRICT, verbose_name="Classe Processual")
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='CADASTRADO')
    data_autuacao = models.DateTimeField(auto_now_add=True)
    relator = models.ForeignKey(Magistrado, on_delete=models.SET_NULL, null=True, blank=True, related_name='processos_relatados')
    processo_prevento = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vinculado por Prevenção:")

    class Meta:
        verbose_name = "Processo Judicial"
        verbose_name_plural = "Processos Judiciais"
    
    def __str__(self):
        return f"Proc. {self.numero} - {self.classe_processual.sigla}"
    
class EstadoExclusao(models.Model):
    MOTIVO_CHOICES = [
        ('AFASTAMENTO', 'Afastamento > 30 dias'),
        ('APOSENTADORIA', '40 dias antes da aposentadoria'),
        ('FERIAS', 'Ferias'),
        ('LICENCA', 'Licença Médica'),
    ]    

    magistrado = models.ForeignKey(Magistrado, on_delete=models.CASCADE)
    motivo = models.CharField(max_length=30, choices=MOTIVO_CHOICES)
    data_inicio = models.DateField(verbose_name="Início da Exclusão")
    data_fim = models.DateField(null=True, blank=True, verbose_name="Fim da Exclusão (Se houver)")

    class Meta: 
        verbose_name = "Estado de exclusão"
        verbose_name_plural = "Estados de exclusão"

    def __str__(self):
        return f"{self.magistrado} excluido por {self.get_motivo_display()}"
    
class AtaDistribuicao(models.Model):
    data_hora = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora da Distribuição")
    processo_numero = models.CharField(max_length=50, verbose_name="Número do Processo")
    classe_sigla = models.CharField(max_length=20, verbose_name="Classe")
    magistrado_sorteado = models.CharField(max_length=150, verbose_name="Magistrado Relator")
    tipo_distribuicao = models.CharField(max_length=50, verbose_name="Tipo de Distribuição")
    fundamento_legal = models.TextField(verbose_name="Fundamento Regimental/Legal")

    class Meta:
        verbose_name = "Ata de Distribuição"
        verbose_name_plural = "Atas de Distribuição"

    def __str__(self):
        return f"Ata {self.id} - Proc: {self.processo_numero} ({self.data_hora.strftime('%d/%m/%Y %H:%M')})"
     
        
