from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, "aller_scan/index.html")
