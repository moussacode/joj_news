from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.liste_article, name='liste_article'),
    path('detail/<int:pk>/', views.detail_article, name="detail_article" ),
]