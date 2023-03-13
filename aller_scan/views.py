import os
from django.core.files.storage import FileSystemStorage 
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from .foodscanner import Allergy
from pathlib import Path

MEMBERS = [
    {"name": "Kaung Pyae Htet", "role": "Leader"},
    {"name": "Kyaw Zay Ya Lin Tun", "role": "Mentor"},
    {"name": "Swan Tayza Aung", "role": "Coder"},
    {"name": "Thaw Zin Thant", "role": "Coder"},
    {"name": "Htet Nay Min", "role": "Designer"},
    {"name": "Minn Thant Kyaw", "role": "Designer"}
]

# Create your views here.
def index(request):
    return render(request, "aller_scan/index.html")

def scan(request):
    if request.method == "POST" and request.FILES['file']:
        upload = request.FILES['file']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        og_url = fss.url(file)
        file_url = os.path.abspath(os.getcwd() + fss.url(file))
        try:
            answer = detect_allergens(file_url)
        except:
            answer = "Oops! An error occured and the picture could not be scanned properly."
        return render(request, "aller_scan/results.html", {
            'img_url': og_url,
            'answer': answer.strip().replace("\n", "<br>")
        })
    else:
        return render(request, "aller_scan/scan.html")

def detect_allergens(img_path):
    aller = Allergy()
    aller.img_to_text(img_path)
    reply = aller.chatgpt()
    return reply

def about(request):

    return render(request, "aller_scan/about.html")
