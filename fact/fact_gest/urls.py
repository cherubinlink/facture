from django.urls import path
from fact_gest import views



urlpatterns = [
    path('',views.accueil,name='accueil'),
    
    # accueil user
    path('accueil_user',views.accuei_user,name='accueil-user'),
    
    # entreprise
    path('entreprise',views.entreprise,name='entreprise'),
    
    # produit
    path('produit',views.produit,name='produit'),
    
    # services
    path('services',views.service,name='service'),
    
    # client
    path('client',views.client,name='client'),
    
    # facture
    path('facture',views.facture,name='facture'),
    
    # facture paye
    path('facture_paye',views.facture_paye,name='facture-paye'),
    
    # facture nom paye
    path('facture_nom_paye',views.facture_nom_paye,name='facture-nom-paye'),
    
    # sav
    path('sav',views.sav,name='sav')
]
