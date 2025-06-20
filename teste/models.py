from django.db import models

# 1. تعريف QuerySet مخصص
class PersonQuerySet(models.QuerySet):
    def adults(self):
        return self.filter(age__gte=18)
    
    def teens(self):
        return self.filter(age__gte=13, age__lt=20)

# 2. تعريف Manager مخصص يستخدم QuerySet
class PersonManager(models.Manager):
    def get_queryset(self):
        return PersonQuerySet(self.model, using=self._db)
    
    def adults(self):
        return self.get_queryset().adults()
    
    def teens(self):
        return self.get_queryset().teens()

# 3. تعريف نموذج Person مع Manager المخصص
class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    objects = PersonManager()  # ربط Manager المخصص

    def __str__(self):
        return f"{self.name} ({self.age} years old)"
