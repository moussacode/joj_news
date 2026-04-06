from django import forms
from .models import Categorie

class ArticleFilterForm(forms.Form):
    titre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Rechercher un article...'})
    )
    categorie = forms.ModelChoiceField(
        queryset=Categorie.objects.all(),
        required=False,
        empty_label="Toutes les categories"
    )