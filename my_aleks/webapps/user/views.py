from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
# Create your views here.


def login_view(request):
    if request.method == "GET":
        next_url = request.GET.get("next", "")
        if next_url:
            next_url="?next="+next_url
        return render(request, "Login.html", {"next":next_url})
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        next_url = request.GET.get("next", "/student/index/")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            request.session['username']=username
            return redirect(next_url)
        else:
            return render(request, "Login.html", {"next": next_url})


def logout_view(request):
    logout(request)
    if request.session.get("username"):
        request.session.pop("username")
    return redirect("/login/")

def register(request):
    if request.method == 'GET':
        return render(request, 'portal/register.html')
    else:
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if not username:
            return HttpResponse('no user name')
        if not password:
            return HttpResponse('no password')
    
        try:
            u = User.objects.get_or_create(username=username)
            if u[1] == False:
                return HttpResponse('user name existed')
            u[0].set_password(password)
            u[0].save()
            if email:
                u[0].email = email
                u[0].save()
            return HttpResponse('OK')
        except Exception as e:
            return HttpResponse('create user failed')
