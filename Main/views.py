from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        return render(request, 'Main/Login/login.html')


def register(request):
    if request.method == 'POST':
        # USER INFO
        username = request.POST['username']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        password = request.POST['password']
        confirm = request.POST['confirmPass']
        email = request.POST['email']
        address = request.POST['address']

        # STORE INFO
        storeName = request.POST['storeName']
        storeAddress = request.POST['storeAddress']

        if password != confirm:
            return render(request, 'Main/Login/register.html', {
                'error_message': 'Passwords do not match.'
            })

        try:
            newUser = User(username=username, first_name=firstName, last_name=lastName,
                           password=password, email=email)
            newUser.save()
        except IntegrityError:
            return render(request, 'Main/Login/register.html', {
                'error_message': 'User already exists.'
            })

        login(request, newUser)
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return render(request, 'Main/Login/register.html')


def dashboard(request):
    user = request.user
    return render(request, 'Main/Landing/dashboard.html', {
        'user': user
    })