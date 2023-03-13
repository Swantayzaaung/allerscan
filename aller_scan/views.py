import os
from django.core.files.storage import FileSystemStorage 
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm

# Create your views here.
def index(request):
    return render(request, "aller_scan/index.html")

def handle_uploaded_file(f):
    print(f)

def scan(request):
    if request.method == "POST" and request.FILES['file']:
        upload = request.FILES['file']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        detect_allergens(file_url)
        return render(request, "aller_scan/results.html", {
            'file_url': file_url
        })
    else:
        return render(request, "aller_scan/scan.html")

def about(request):
    return render(request, "aller_scan/about.html")
