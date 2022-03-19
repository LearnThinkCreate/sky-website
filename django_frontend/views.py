from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'django_frontend/index.html')

def login_view(request):
    # Checking for valid request
    if request.method != "GET":
        return JsonResponse({"Error":"Invalid web requests"})

    # Getting Blackbaud users info
    try:
        token = request.GET["ssotoken"]
        print('Authenticating')
        user = authenticate(request, token=token)
        print('Sucessful')
    except MultiValueDictKeyError:
        return redirect("https://tampaprep.myschoolapp.com/app/sso/auth/testing")

    # Logging the user in
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return redirect("https://tampaprep.myschoolapp.com/app/sso/auth/testing")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('https://tampaprep.myschoolapp.com/app#login')

