from django.views.generic import TemplateView
from django.shortcuts import render


def index(request):
    return render(request, 'index.html', context={
        'who': 'Python-project-52',
    })


def about(request):
    return render(request, 'about.html')




