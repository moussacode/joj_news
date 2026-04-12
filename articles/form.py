from django import forms
from .models import Categorie, Commentaire

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

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ajouter un commentaire...'}),
        }
    
