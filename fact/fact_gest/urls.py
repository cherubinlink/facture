from django.urls import path
from fact_gest import views



urlpatterns = [
    path('',views.accueil,name='accueil'),
    
    # accueil user
    path('accueil_user',views.accuei_user,name='accueil-user'),
    
    # produit
    path('produit',views.produit,name='produit')
]
