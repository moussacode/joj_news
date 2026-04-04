from django.shortcuts import render , get_object_or_404
from . import models
from django.core.paginator import Paginator
# Create your views here.

def home (request):
    return render(request ,'base.html')

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