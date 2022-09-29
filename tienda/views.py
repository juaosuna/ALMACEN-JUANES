from django.shortcuts import render
from multiprocessing import context

def home(request):
    return render(request, 'home.html')

def verContactenos(request):
    return render(request, 'contactenos.html')

def nosotros(request):
    return render(request, 'nosotros.html')

