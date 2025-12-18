from django.shortcuts import render

def login(request):
    return render(request, 'ACC/login.html')

def dashboard(request):
    return render(request, 'ACC/dashboard.html')

def accidentes(request):
    return render(request, 'ACC/accidentes.html')
