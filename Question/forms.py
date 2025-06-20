from django import forms 
from .models import Question,Opinions
from django.contrib.auth import get_user_model

User = get_user_model()

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['doctor', 'question_text'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(user_type='doctor')  
