from django.shortcuts import render
from .models import Person

# عرض كل الأشخاص
def all_people(request):
    people = Person.objects.all()
    return render(request, 'test2.html', {'people': people})

# عرض الأشخاص البالغين (عمرهم 18 وفوق)
def adults(request):
    adults = Person.objects.adults()
    return render(request, 'test2.html', {'people': adults})

# عرض المراهقين (13 إلى أقل من 20)
def teens(request):
    teens = Person.objects.teens()
    return render(request, 'test2.html', {'people': teens})
