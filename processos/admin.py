from django.contrib import admin
from .models import Processo
from .models import Processo, ConflitoInteresse

@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'documento', 'nivel', 'status', 'juiz_responsavel', 'reaberto')
    list_filter = ('nivel', 'status', 'reaberto')
    search_fields = ('numero', 'documento')

@admin.register(ConflitoInteresse)
class ConflitoInteresseAdmin(admin.ModelAdmin):
    list_display = ('processo', 'juiz', 'data_registro')
    list_filter = ('data_registro',)
    search_fields = ('processo__numero', 'juiz__username')