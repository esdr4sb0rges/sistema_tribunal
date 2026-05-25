from django.contrib import admin
from .models import Magistrado, ClasseProcessual, Processo, EstadoExclusao, AtaDistribuicao


@admin.register(Magistrado)
class MagistradoAdmin(admin.ModelAdmin):
    list_display = ('user', 'saldo_processos', 'genero')
    search_fields = ('user__username', 'user__first_name')
    filter_horizontal = ('parentes',)

@admin.register(ClasseProcessual)
class ClasseProcessualAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nome', 'orgao_competente', 'ativo')
    list_filter = ('orgao_competente', 'ativo')
    search_fields = ('sigla', 'nome')

@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'classe_processual', 'status', 'relator', 'processo_prevento')
    list_filter = ('status', 'classe_processual__orgao_competente')
    search_fields = ('numero',)

@admin.register(EstadoExclusao)
class EstadoExclusaoAdmin(admin.ModelAdmin):
    list_display = ('magistrado', 'motivo', 'data_inicio', 'data_fim')
    list_filter = ('motivo',)

@admin.register(AtaDistribuicao)
class AtaDistribuicaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_hora', 'processo_numero', 'classe_sigla', 'magistrado_sorteado', 'tipo_distribuicao')
    list_filter = ('tipo_distribuicao', 'data_hora')
    search_fields = ('processo_numero', 'magistrado_sorteado')
    
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False