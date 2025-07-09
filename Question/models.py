from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from clinic.models import TimeStampeModel
from django.contrib.auth import get_user_model

User = get_user_model()  

class Question(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_questions')
    question_text = models.TextField()
    answer_text = models.TextField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return f"Question from {self.patient} to {self.doctor}"
    
class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE , related_name='notifications')
    message = models.TextField()
    url = models.URLField(blank=True , null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    
class Opinions(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='Opinions')
    comment = models.TextField()
    evaluation=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.user.username} - {self.evaluation} Stars"