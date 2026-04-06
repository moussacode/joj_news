from django.shortcuts import render , get_object_or_404, redirect
from . import models
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.

def home (request):
    return render(request ,'home.html')

def liste_article (request):
    liste_article = models.Article.objects.all()

    pagination = Paginator(liste_article,2)

    page_number = request.GET.get('page')
    article = pagination.get_page(page_number) 

    contexte ={
       
        'liste_article': article,
    }
    
    return render(request,"liste_articles.html",contexte)

def detail_article (request,pk):
    
    article = get_object_or_404(models.Article,pk=pk) 
    contexte={
        'article':article
    }
    return render(request,"detail-article.html",contexte)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False  # IMPORTANT
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})