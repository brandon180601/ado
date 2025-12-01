from django.shortcuts import render

def index(request):
    return render(request, 'ACC/index.html')

def main(request):
    return render(request, 'ACC/main.html')
