from django.contrib import admin
from polls.models import Evento

class EventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'data_evento', 'data_criacao')
    list_filter = ('usuario',)

admin.site.register(Evento, EventoAdmin)
