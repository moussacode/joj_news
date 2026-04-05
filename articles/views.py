from django.shortcuts import render , get_object_or_404
from . import models
from django.core.paginator import Paginator
from .form import ArticleFilterForm
# Create your views here.

def home (request):
    return render(request ,'home.html')

def liste_article (request):
    liste_article = models.Article.objects.all()

    form = ArticleFilterForm(request.GET or None)
    
    if form.is_valid():
        titre = form.cleaned_data.get('titre')
        categorie = form.cleaned_data.get('categorie')
        

        if titre:
            liste_article = liste_article.filter(titre__icontains=titre)

        if categorie:
            liste_article = liste_article.filter(categorie=categorie)

    pagination = Paginator(liste_article,2)

    page_number = request.GET.get('page')
    article = pagination.get_page(page_number) 

    contexte ={
        'form':form,
        'liste_article': article,
    }
    
    return render(request,"liste_articles.html",contexte)

def detail_article (request,pk):
    
    article = get_object_or_404(models.Article,pk=pk) 
    contexte={
        'article':article
    }
    return render(request,"detail-article.html",contexte)