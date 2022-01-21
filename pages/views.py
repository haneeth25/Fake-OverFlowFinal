from email import message
from django.shortcuts import redirect, render
from . models import Messages, Room, Topic
from . forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate , login , logout

# Create your views here.


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User doesnot exist')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Password wrong')
    context = {}
    return render(request,'pages/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def createUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        try:
            user = User.objects.create_user(username=username,
                                    email=email,
                                    password=password1)
            login(request,user)
            return redirect('home')
        except:
            messages.error(request,'username or email already taken')
    context = {}
    return render(request,'pages/register.html',context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q')!= None else ''
    room = Room.objects.filter(
        Q(topic__topicName__icontains=q)|
        Q(name__icontains = q) |
        Q(description__icontains = q)
    )
    topics = Topic.objects.all().distinct()
    context = {'room':room , 'topics':topics}
    return render(request,'pages/home.html',context)

def qna(request,pk):
    room = Room.objects.get(id=pk)
    answer  = room.messages_set.all().order_by('-created')
    if request.method == 'POST':
        answer = Messages.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        return redirect('qna', pk=room.id)
    context = {'room':room,'answer':answer}
    return render(request,'pages/qna.html',context)

def profile(request):
    pk = request.user.id
    user = User.objects.get(id = pk )
    room = user.room_set.all()
    message = user.messages_set.all()
    context = {'room':room , 'answer':message}
    return render(request,'pages/profile.html',context)

@login_required(login_url='/login')
def createQuestion(request):
    if request.method == 'POST':
        topic = request.POST.get('topic').lower()
        topics,created = Topic.objects.get_or_create(topicName = topic)
        question = request.POST.get('Heading')
        description = request.POST.get('description')
        form = Room(
            host = request.user,
            topic = topics,
            name = question,
            description = description
            )
        form.save()
        return redirect('home')
    context = {}
    return render(request,'pages/question_create.html',context)
@login_required(login_url='/login')
def deleteQuestion(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You can't delete question")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'pages/delete.html',{'obj':room})
@login_required(login_url='/login')
def deleteAnswer(request,pk):
    answer = Messages.objects.get(id=pk)
    if request.user != answer.user:
        return HttpResponse("You can't delete question")
    if request.method == 'POST':
        answer.delete()
        return redirect('home')
    return render(request,'pages/delete.html',{'obj':answer})


