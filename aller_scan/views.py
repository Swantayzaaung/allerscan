from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    return render(request, "aller_scan/index.html")

def scan(request):
    return HttpResponse("scan")

def about(request):
    return HttpResponse("about")

def account(request):
    return HttpResponse("account")

def login(request):
    return HttpResponse("login")

def edit(request):
    return HttpResponse("edit")