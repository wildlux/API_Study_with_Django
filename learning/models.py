from django.db import models

class Question(models.Model):
    QUESTION_TYPES = [
        ('closed', 'Chiusa'),
        ('open', 'Aperta'),
    ]

    text = models.TextField(verbose_name="Testo della domanda")
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='closed', verbose_name="Tipo di domanda")
    options = models.JSONField(blank=True, null=True, verbose_name="Opzioni (per domande chiuse)", help_text="Lista di opzioni, es. ['a) Opzione 1', 'b) Opzione 2']")
    correct_answer = models.CharField(max_length=10, verbose_name="Risposta corretta", help_text="Per chiuse: lettera (a,b,c,d); per aperte: testo esatto")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordine")
    active = models.BooleanField(default=True, verbose_name="Attiva")

    class Meta:
        ordering = ['order']
        verbose_name = "Domanda Quiz"
        verbose_name_plural = "Domande Quiz"

    def __str__(self):
        return f"Domanda {self.order}: {self.text[:50]}..."
