from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from urllib.parse import quote

from .forms import QuestionForm, Question_chatForm, Answer_chatForm
from .models import Question, Notification, Opinions


@login_required
def ask_doctor(request):
    questions = Question.objects.filter(patient=request.user)
    form = QuestionForm()

    if request.method == 'POST' and 'ask_button' in request.POST:
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.patient = request.user
            question.save()

            doctor = question.doctor
            doctor_id = doctor.id
            message = "📩 New question from a patient."

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{doctor_id}",
                {
                    'type': 'send_notification',
                    'message': message,
                }
            )

            Notification.objects.create(
                user=doctor,
                message=f"🆕 The patient {request.user.username} sent you a question.",
                url=f"/questions/{question.id}/"
            )

            # Suggestion: Consider externalizing the WhatsApp URL generation to a utility function
            if hasattr(doctor, 'phone') and doctor.phone:
                msg = f"New question from {request.user.username}:\n\n{question.question_text}"
                encoded = quote(msg)
                whatsapp_url = f"https://wa.me/{doctor.phone}?text={encoded}"
                messages.success(request, "Your question has been successfully sent!")
                return render(request, 'temp/redirect_to_whatsapp.html', {
                    'whatsapp_url': whatsapp_url
                })
            else:
                messages.warning(request, "Doctor doesn't have a phone number registered.")
                return redirect('ask_doctor')

    elif request.method == 'POST' and 'send_rating' in request.POST:
        evaluation = request.POST.get('evaluation')
        comment = request.POST.get('comment')
        if evaluation and comment:
            Opinions.objects.create(
                user=request.user,
                comment=comment,
                evaluation=int(evaluation)
            )
            messages.success(request, "Your evaluation has been sent successfully.")
        else:
            messages.error(request, "Please fill in all fields.")
        return redirect('ask_doctor')

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

        patient_id = question.patient.id
        message = "📩 Your question has been answered."

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{patient_id}",
            {
                'type': 'send_notification',
                'message': message,
            }
        )

        Notification.objects.create(
            user=question.patient,
            message=f"The doctor {question.doctor.first_name} answered your question.",
            url=f"/questions/{question.id}/"
        )

        messages.success(request, "The answer has been sent successfully.")
        return redirect('question_detail', pk=question.pk)

    return render(request, 'temp/answer_question.html', {'question': question})


@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    Notification.objects.filter(user=request.user, url=f"/questions/{pk}/").update(is_read=True)
    return render(request, 'question_detail.html', {'question': question})


@login_required
def ask_doctor_chat(request):
    if request.method == 'POST':
        form = Question_chatForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.patient = request.user
            question.save()

            # Sending WebSocket notification to doctor
            doctor_id = question.doctor.id
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{doctor_id}",
                {
                    'type': 'send_notification',
                    'message': f"🆕 NEW Question from {request.user.username}",
                    'text': question.question_text,
                    'sender': request.user.get_full_name() or request.user.username,
                    'timestamp': question.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                }
            )

            return JsonResponse({
                'success': True,
                'question_id': question.id,
                'question_text': question.question_text,
                'timestamp': question.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            })

        return JsonResponse({'success': False, 'errors': form.errors})

    # GET method returns latest  questions
    questions = Question.objects.filter(patient=request.user).order_by('-timestamp')
    form = Question_chatForm()
    return render(request, 'base.html', {'form': form, 'questions': questions})


@login_required
def answer_question_chat(request, pk):
    question = get_object_or_404(Question, pk=pk, doctor=request.user)

    if request.method == 'POST':
        form = Answer_chatForm(request.POST, instance=question)
        if form.is_valid():
            q = form.save(commit=False)
            q.answered_at = timezone.now()
            q.save()

            patient_id = question.patient.id
            message = "📩 Your question has been answered."

            # Send WebSocket notification to patient
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{patient_id}",
                {
                    'type': 'send_notification',
                    'message': message,
                    'text': q.answer_text,
                    'sender': question.doctor.get_full_name() or question.doctor.username,
                    'timestamp': q.answered_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
            )

            Notification.objects.create(
                user=question.patient,
                message=f"The doctor {question.doctor.first_name} answered your question.",
                url=f"/questions/{question.id}/"
            )

            return JsonResponse({
                'success': True,
                'answer_text': q.answer_text,
                'timestamp': q.answered_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        return JsonResponse({'success': False, 'errors': form.errors})

    form = Answer_chatForm(instance=question)
    return render(request, 'base.html', {'form': form, 'question': question})
