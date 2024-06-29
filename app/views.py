from django.shortcuts import render, redirect

def home(request):
    return render(request, 'app/home.html')

def wiki(request):
    return render(request, 'app/wiki.html')

def links(request):
    return render(request, 'app/links.html')