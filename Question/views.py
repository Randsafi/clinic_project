from django.shortcuts import render, redirect, get_object_or_404 
from django.http import JsonResponse
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from urllib.parse import quote
from .forms import QuestionForm,Question_chatForm,Answer_chatForm
from .models import Question, Notification, Opinions



@login_required
def ask_doctor(request):
    questions = Question.objects.filter(patient=request.user)
    form = QuestionForm()  # تعيين مبدئي دائم

    if request.method == 'POST':
        if 'ask_button' in request.POST:
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.patient = request.user
                question.save()

                doctor = question.doctor

                # 🔔 إشعار داخلي للدكتور
                Notification.objects.create(
                    user=doctor,
                    message=f"🆕 the patient {request.user.username} I sent you a question.",
                    url=f"/questions/{question.id}/"
                )

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

        elif 'send_rating' in request.POST:
            evaluation = request.POST.get('evaluation')
            comment = request.POST.get('comment')
            if evaluation and comment:
                Opinions.objects.create(
                    user=request.user,
                    comment=comment,
                    evaluation=int(evaluation)
                )
                messages.success(request, "Your evaluation has been sent successfully.")
                return redirect('ask_doctor')
            else:
                messages.error(request, "Please fill in all fields.")

    return render(request, 'temp/ask_question.html', {
        'form': form,
        'questions': questions
    })


@login_required
def answer_question(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.user != question.doctor:
        return HttpResponseForbidden("You are not allowed to answer this question.")

    if request.method == 'POST':
        answer = request.POST.get('answer')
        question.answer_text = answer
        question.answered_at = timezone.now()
        question.save()

        Notification.objects.create(
            user=question.patient,
            message=f" the doctor {question.doctor.first_name} Answered your question.",
            url=f"/questions/{question.id}/"
        )

        messages.success(request, "The answer has been sent successfully.")
        return redirect('question_detail', pk=question.pk)

    return render(request, 'temp/answer_question.html', {'question': question})

@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)

    # تحديث أي إشعار غير مقروء متعلق بهذا السؤال
    Notification.objects.filter(user=request.user, url=f"/questions/{pk}/").update(is_read=True)

    return render(request, 'question_detail.html', {'question': question})

from django.shortcuts import redirect

@login_required 
def ask_doctor_chat(request):
    questions = Question.objects.filter(patient=request.user).order_by('timestamp')
    form = Question_chatForm()

    if request.method == 'POST':
        form = Question_chatForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.patient = request.user
            question.save()
            doctor = question.doctor

            # 🔔 إشعار داخلي للدكتور
            Notification.objects.create(
                user=doctor,
                message=f"🆕 the patient {request.user.username} I sent you a question.",
                url=f"/questions/{question.id}/"
            )
            return redirect('/')  # غيّر الاسم حسب ما سمّيت الـ url

    return render(request, 'base.html', {
        'form': form,
        'questions': questions,
    })

@login_required
def answer_question_chat(request, pk):
    question = get_object_or_404(Question, pk=pk, doctor=request.user)

    if request.method == 'POST':
        form = Answer_chatForm(request.POST, instance=question)
        if form.is_valid():
            q = form.save(commit=False)
            q.answered_at = timezone.now()
            q.save()
            Notification.objects.create(
                    user=question.patient,
                    message=f" the doctor {question.doctor.first_name} Answered your question.",
                    url=f"/questions/{question.id}/"
                )
            return redirect('/')  # صفحة الأسئلة الواردة للدكتور
    else:
        form = Answer_chatForm(instance=question)

    return render(request, 'base.html', {'form': form, 'question': question})


