from django.shortcuts import render , get_object_or_404, redirect
from . import models
from django.core.paginator import Paginator
from .form import ArticleFilterForm, CommentaireForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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
    commentaires = article.commentaires.all()
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentaireForm(request.POST)
            if form.is_valid():
                commentaire = form.save(commit=False)
                commentaire.utilisateur = request.user
                commentaire.article = article
            commentaire.save()
            return redirect('article_detail', pk=article.pk)
        else:
            # rediriger vers login si pas connecté
            return redirect('login')
    contexte={
        'article': article,
        'commentaires': commentaires,
        'form': form
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


# 🔹 Afficher article + ajouter commentaire
def detail_article(request, id):
    article = get_object_or_404(models.Article, id=id)
    commentaires = article.commentaires.filter(actif=True)

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentaireForm(request.POST)
            if form.is_valid():
                commentaire = form.save(commit=False)
                commentaire.utilisateur = request.user
                commentaire.article = article
                commentaire.save()
                return redirect('detail_article', id=article.id)
        else:
            return redirect('login')
    else:
        form = CommentaireForm()

    return render(request, 'detail_article.html', {
        'article': article,
        'commentaires': commentaires,
        'form': form
    })


# 🔹 Modifier commentaire
def modifier_commentaire(request, id):
    commentaire = get_object_or_404(models.Commentaire, id=id)

    if commentaire.utilisateur != request.user:
        return redirect('detail_article', id=commentaire.article.id)

    if request.method == 'POST':
        form = CommentaireForm(request.POST, instance=commentaire)
        if form.is_valid():
            form.save()
            return redirect('detail_article', id=commentaire.article.id)
    else:
        form = CommentaireForm(instance=commentaire)

    return render(request, 'modifier_commentaire.html', {'form': form})


# 🔹 Supprimer commentaire
def supprimer_commentaire(request, id):
    commentaire = get_object_or_404(models.Commentaire, id=id)

    if commentaire.utilisateur != request.user:
        return redirect('detail_article', id=commentaire.article.id)

    commentaire.delete()
    return redirect('detail_article', id=commentaire.article.id)