from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import QuestionForm
from .models import Question,Notification
from django.contrib.auth.decorators import login_required
from urllib.parse import quote

@login_required
def ask_doctor(request):
    questions=Question.objects.all()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.patient = request.user
            question.save()
            doctor = question.doctor

            if hasattr(doctor, 'phone') and doctor.phone:
                message = f"New question from {request.user.username}:\n\n{question.question_text}"
                encoded_message = quote(message)
                whatsapp_url = f"https://wa.me/{doctor.phone}?text={encoded_message}"
                messages.success(request, "Your question has been successfully sent!")
                return render(request, 'temp/redirect_to_whatsapp.html', {
                    'whatsapp_url': whatsapp_url
                })
            else:
                messages.warning(request, "Doctor doesn't have a phone number registered.")
                return redirect('ask_doctor')
    else:
        form = QuestionForm()
    
    return render(request, 'temp/ask_question.html', {
        'form': form ,
        'questions':questions})

def answer_question(request , pk):
    try:
        question=Question.objects.get(pk = pk)
    except Question.DoesNotExist:
        return render(request, 'parts1/404.html' , status=404)
    
    if request.method == 'POST':
        answer = request.post.get('answer')
        question.answer_text = answer
        question.save()

        Notification.objects.create(
            user = question.patient ,
            message=f"Dr. {question.doctor.first_name} answered your question."
            url = f""
        )
        return redirect()
    

def question_detail(request, pk):
    try:
        question=Question.objects.get(pk = pk)
    except Question.DoesNotExist:
        return render(request, 'parts1/404.html' , status=404)
    
    Notification.objects.filter(user=request.user, link=f"/questions/{pk}/").update(is_read=True)
    # حدد الإشعار كمقروء إذا فيه واحد مرتبط بهالسؤال

    return render(request, 'question_detail.html', {'question': question})

