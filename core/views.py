from django.http import JsonResponse
from django.shortcuts import render


def homepage(request):
    return render(request, 'pages/index.html')


def login(request):
    return render(request, 'pages/login.html')
