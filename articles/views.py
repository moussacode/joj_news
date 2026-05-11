from django.shortcuts import render , get_object_or_404, redirect
from . import models
from django.core.paginator import Paginator
from .form import ArticleFilterForm, CommentaireForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy

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
    commentaires = article.commentaires.all().order_by('-date_commentaire')
    form = CommentaireForm()
    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.article = article
            commentaire.user = request.user
            commentaire.save()
            return redirect('detail_article', pk=article.pk)

    contexte={
        'article':article,
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

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Commentaire
    template_name = 'commentaire_form.html'
    fields = ['contenu']
    def get_success_url(self):
        article = self.get_object().article
        return reverse_lazy('detail_article', kwargs={'pk': article.pk})

    def test_func(self):
        commentaire = self.get_object()
        return self.request.user == commentaire.user
    
