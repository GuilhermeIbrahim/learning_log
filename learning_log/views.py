from django.shortcuts import render, get_object_or_404
from .models import Topic, Entry, Category
from .forms import CategoryForm, TopicForm, EntryForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count

def index(request):
    """Página principal do Learning_log"""
    return render(request, 'learning_log/index.html')

@login_required
def topics(request):
    """Mostra todos os assuntos"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_log/topics.html', context)

@login_required
def topic(request, topic_id):
    """Mostra um único assunto e todas as suas entradas"""
    topic = get_object_or_404(Topic, id = topic_id)
    
    # Garante que o assunto pertence ao usuário atual
    if topic.owner != request.user:
        raise Http404
    
    entries_list = topic.entry_set.order_by('-date_added')
    
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    
    if query:
        entries_list = entries_list.filter(text__icontains=query)
    
    if category_id:
        entries_list = entries_list.filter(categories__id=category_id)
    
    entries_list = entries_list.distinct()
    paginator = Paginator(entries_list, 5)
    page_number = request.GET.get('page')
    entries = paginator.get_page(page_number)
    categories = Category.objects.filter(owner=request.user).order_by('name')
    
    context = {'topic': topic, 'entries': entries, 'categories': categories, 'query': query, 'selected_category': category_id}
    return render(request, 'learning_log/topic.html', context)

@login_required
def new_topic(request):
    """Adiciona um novo assunto."""
    if request.method != 'POST':
        # Nenhum dado submetido; cria um formulário em branco.
        form = TopicForm()
    else:
        # Dados de POST submetidos; processa os dados.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))
        
    context = {'form': form}
    return render(request, 'learning_log/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Acrescenta uma nova entrada para um assunto em particular."""
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Garante que o assunto pertence ao usuário atual
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # Nenhum dado submetido; cria um formulário em branco.
        form = EntryForm(user=request.user)
    else:
        # Dados de POST submetidos; processa os dados.
        form = EntryForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            form.save_m2m()  # Salva as relações ManyToMany
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
    
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_log/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edita uma entrada existente."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    
    # Garante que o assunto pertence ao usuário atual
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # Requisição inicial; preenche previamente o formulário com a entrada atual.
        form = EntryForm(instance=entry, user=request.user)
    else:
        # Dados de Post submetidos; processa os dados.
        form = EntryForm(instance=entry, data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_log/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    """Exclui uma entrada existente."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    
    # Garante que o assunto pertence ao usuário atual
    if topic.owner != request.user:
        raise Http404
    
    if request.method == 'POST':
        entry.delete()
        return HttpResponseRedirect(reverse('topic', args=[topic.id]))
        
    
    context = {'entry': entry, 'topic': topic}
    return render(request, 'learning_log/delete_entry.html', context)
    
@login_required
def new_category(request):
    """Adiciona uma nova categoria."""
    if request.method != 'POST':
        # Nenhum dado submetido; cria um formulário em branco.
        form = CategoryForm(user=request.user)
    else:
        # Dados de POST submetidos; processa os dados.
        form = CategoryForm(request.POST, user=request.user)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.owner = request.user
            new_category.save()
            return HttpResponseRedirect(reverse('topics'))

    context = {'form': form}
    return render(request, 'learning_log/new_category.html', context)

@login_required
def dashboard(request):
    """Mostra o dashboard do usuário com estatísticas e gráficos."""
    topics_count = Topic.objects.filter(owner=request.user).count()
    entries_count = Entry.objects.filter(topic__owner=request.user).count()
    categories_count = Category.objects.filter(owner=request.user).count()
    recent_entries = Entry.objects.filter(topic__owner=request.user).order_by('-date_added')[:5]
    top_categories = Category.objects.filter(owner=request.user).annotate(total_entries=Count('entry')).order_by('-total_entries')[:5]

    context = {'topics_count': topics_count, 'entries_count': entries_count, 'categories_count': categories_count, 'recent_entries': recent_entries, 'top_categories': top_categories}
    return render(request, 'learning_log/dashboard.html', context)