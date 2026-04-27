from django.urls import path
from .views import register
from . import views
from .views import detail_article, modifier_commentaire, supprimer_commentaire
urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.liste_article, name='liste_article'),
    path('detail/<int:id>/', views.detail_article, name="detail_article" ),
    path('register/', register, name='register'),
    path('commentaire/modifier/<int:id>/', modifier_commentaire, name='modifier_commentaire'),
    path('commentaire/supprimer/<int:id>/', supprimer_commentaire, name='supprimer_commentaire'),

]