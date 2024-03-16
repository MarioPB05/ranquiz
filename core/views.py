from django.http import JsonResponse
from django.shortcuts import render


def homepage(request):
    # Enviar un hola mundo en json
    return render(request, 'pages/index.html')
