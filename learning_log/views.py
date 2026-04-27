from django.shortcuts import render
from .models import Topic

def index(request):
    """Página principal do Learning_log"""
    return render(request, 'learning_log/index.html')

def topics(request):
    """Mostra todos os assuntos"""
    topic = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_log/topics.html', context)