from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.db import IntegrityError
from .models import BoardModel
from django.views.generic import CreateView
from django.urls import reverse_lazy
def signup_func(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username,
                                    '',
                                    password)
            return render(request, 'signup.html', {'some':100})
        except IntegrityError:
            print('IntegrityErrorです。')
            return render(request, 'signup.html', {'error':'このユーザがすでに登録されています。'})
        except ValueError:
            print('ValueErrorです。')
            return render(request, 'signup.html', {'error':'フォームに値を入力してください。'})
    return render(request, 'signup.html', {'some':100})

def login_func(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return render(request, 'login.html',{})
    return render(request, 'login.html',{'context': 'get method'})

@login_required
def list_func(request):
    object_list = BoardModel.objects.all()
    return render(request, 'list.html',{'object_list':object_list})

def logout_func(request):
    logout(request)
    return redirect('login')

def detail_func(request,pk):
    object = get_object_or_404(BoardModel,pk=pk)
    username = request.user.get_username()
    return render(request,'detail.html',{'object':object, 'username': username})

def good_func(request,pk):
    object = BoardModel.objects.get(pk=pk)
    object.good = object.good + 1
    object.save()
    return redirect('list')

def read_func(request,pk):
    object = BoardModel.objects.get(pk=pk)
    username = request.user.get_username()
    if username in object.readtext:
        return redirect('list')
    else:
        object.read += 1
        object.readtext = object.readtext + ',' + username
        object.save()
        return redirect('list')
    
class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BoardModel
    fields ={'title', 'content', 'author','sns_image'}
    success_url = reverse_lazy('list')