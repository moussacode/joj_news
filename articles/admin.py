from django.contrib import admin
from .models import Categorie, Article


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'date_publication')
    list_filter = ('categorie', 'date_publication')
    search_fields = ('titre', 'contenu')
    date_hierarchy = 'date_publication'
    ordering = ('-date_publication',)