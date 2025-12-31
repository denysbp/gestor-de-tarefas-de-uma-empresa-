from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.contrib.auth.models import User
from django.dispatch import receiver
from  django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Employeer,Task
from django.http import JsonResponse
from .models import Task, TaskUpload
from time import sleep
# Create your views here.

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Dados invalidos,você não tem acesso!')
            return redirect('/')
    else:
        return render(request,'login.html')

def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        password1=request.POST.get('password1')
        email=request.POST.get('email')
        if password==password1:
            if User.objects.filter(email=email).exists():
                messages.error(request,'Este email já esta em uso')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                    messages.error(request,'Nome de usuario já existente')
                    return redirect('register')
            else:
                user=User.objects.create_user(username=username,password=password,email=email)
                employeer=Employeer.objects.create(user=user,email=email)
                user.save()
                employeer.save()
                return redirect('/')
        else:
            messages.error(request,'As passwords não são iguais')
            return redirect('register')
    else:
        return render(request,'register.html')
def log_out(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    employeer = request.user.employeer # pega o funcionário logado
    tasks = Task.objects.filter(empregador=employeer)# busca tasks dele
    return render(request,'home.html',{
        'username':request.user.username,
        'email':request.user.employeer.email,
        'cargo':request.user.employeer.cargo,
        'foto':employeer.foto,
        'tasks': tasks,
    })

@receiver(user_logged_in)
def set_online(sender,request,user,**kwargs):
    user.employeer.Online=True
    user.employeer.save()


@receiver(user_logged_out)
def set_offline(sender,user,request,**kwargs):
    user.employeer.Online=False
    user.employeer.save()


def upload_task_files(request):
    if request.method == "POST": 
        task_id = request.POST.get("task_id")
        task = Task.objects.get(id=task_id)

        for file in request.FILES.getlist("files"):
            TaskUpload.objects.create(
                task=task,
                file=file
            )
        return JsonResponse({"status": "ok"})
    
def reset(request):
    if request.method=='POST':
        email=request.POST.get('email')
        print(User.objects.values_list('email', flat=True))
        if User.objects.filter(email=email).exists():
            return redirect('done')
        else:
            messages.error(request,'Esse email não esta registrado com nenhum usuario')
    print(User.objects.values_list('email', flat=True))
    return render(request,'password_reset.html')

def done_reset(request):
    return render(request,'password_reset_done.html')

def new_password(request):
    return render(request,'new_password.html')