from django.db import models
from django.contrib.auth.models import User




class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom


class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='articles')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.titre
    
class Commentaire(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_commentaire = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires')
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"Commentaire de {self.utilisateur} sur {self.article}"
    