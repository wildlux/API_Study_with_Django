from django.contrib import admin
from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_type', 'correct_answer', 'order', 'active')
    list_filter = ('question_type', 'active')
    search_fields = ('text', 'correct_answer')
    ordering = ('order',)

    fieldsets = (
        ('Informazioni Base', {
            'fields': ('text', 'question_type', 'order', 'active')
        }),
        ('Risposte', {
            'fields': ('options', 'correct_answer'),
            'description': 'Per domande chiuse: lista di opzioni come ["a) Opzione 1", "b) Opzione 2"]. Per aperte: lascia options vuoto.'
        }),
    )
