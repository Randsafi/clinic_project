from django.contrib import admin
from .models import Question
# Register your models here.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'timestamp', 'answer_text']
    search_fields = ['question_text', 'answer_text']