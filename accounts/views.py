from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from .forms import DoctorForm,PatientForm
from django.contrib.auth import get_user_model
User = get_user_model()

def custom_404_view(request, exception):
    return render(request, 'parts1/404.html', status=404)

# Create your views here.
def register(request):
    if request.method == 'POST':
        form =CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data['user_type']
            request.session['partial_user_id'] = user.id
            return redirect('register2', user_type=user_type)
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html' , {'form':form})

def register2(request,user_type):
    user_id = request.session.get("partial_user_id")
    if not user_id:
        return redirect('register')
    
    user = User.objects.get(id = user_id)

    if request.method == 'POST':
        if user_type == 'doctor' :
            form = DoctorForm(request.POST)
            if form.is_valid():
                doctor = form.save(commit=False)
                doctor.user = user
                doctor.save()
                login(request, user)
                return redirect('index')
                
        elif user_type == "patient":
            form = PatientForm(request.POST)
            if form.is_valid():
                patient = form.save(commit=False)
                patient.user = user
                patient.save()
                login(request, user)
                return redirect('index')
        else:
            return redirect('index')
            
    else:
        form = DoctorForm() if user_type == 'doctor' else PatientForm()       

    return render(request , 'accounts/register2.html' , {'form' :form , 'user_type': user_type})
