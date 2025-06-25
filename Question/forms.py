from django import forms 
from .models import Question,Opinions
from django.contrib.auth import get_user_model

User = get_user_model()

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['doctor', 'question_text'] 
        widgets = {
            'question_text': forms.Textarea(attrs={'placeholder': 'Write your question here...'}),
            
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(user_type='doctor')  

class Question_chatForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['doctor', 'question_text']
        widgets = {
            'doctor': forms.Select(attrs={
                'class': 'form-control mb-2',
                'id': 'doctor',
            }),
            'question_text': forms.Textarea(attrs={
                'class': 'form-control rounded',
                'rows': 3,
                'placeholder': 'Write your question here...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = User.objects.filter(user_type='doctor')

