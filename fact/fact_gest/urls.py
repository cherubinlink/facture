from django.urls import path
from fact_gest import views



urlpatterns = [
    path('',views.accueil,name='accueil'),
    
    # accueil user
    path('accueil_user',views.accuei_user,name='accueil-user'),
    
    # group
    path('group',views.voir_group,name='voir-group'),
    
    # detail group
    path('detail_group/<int:group_id>/',views.detail_group,name='detail-group'),
    
    # creer group
    path('creer_group',views.creer_group,name='creer-group'),
    
    # modifeir_group
    path('modifier_group/<int:pk>/',views.modifier_group,name='modifier-group'),
    
    # supprimer group
    path('supprimer_group/<int:pk>/',views.supprimer_group,name='supprimer-group'),
    
    # entreprise
    path('entreprise/<int:pk>/',views.entreprise,name='entreprise'),
    
    # creer une entreprise
    path('creer_entreprise/',views.creer_entreprise,name='creer-entreprise'),
    
    # modifier entreprise
    path('modifier_entreprise/<int:pk>/',views.modifier_entreprise,name='modifier-entreprise'),
    
    # supprimer entreprise
    path('supprimer_entreprise/<int:pk>/',views.supprimer_entreprise,name='supprimer-entreprise'),
    
    # produit
    path('produit/<int:entreprise_id>/',views.produit,name='produit'),
    
    # ajouter produit
    path('ajouter_produit/<int:entreprise_id>/produit/ajouter/',views.ajouter_produit,name='ajouter-produit'),
    
    # modifier produit
    path('modifier_produit/<int:produit_id>/',views.modifier_produit,name='modifier-produit'),
    
    # supprimer produit
    path('entreprise/<int:entreprise_id>/supprimer_produit/', views.supprimer_produit, name='supprimer_produit'),
    
    # services
    path('services',views.service,name='service'),
    
    # client
    path('client/<int:entreprise_id>/',views.client,name='client'),
    
    # ajouter un client
    path('ajouter_client/<int:entreprise_id>/clients/ajouter/',views.ajouter_client,name='ajouter-client'),
    
    # modifier un client
    path('modifier_client/<int:client_id>/',views.modifier_client,name='modifier-client'),
    
    # supprimer client
    path('entreprise/<int:entreprise_id>/supprimer_clients/', views.supprimer_clients, name='supprimer_clients'),
    
    # facture
    path('facture',views.facture,name='facture'),
    
    # facture paye
    path('facture_paye',views.facture_paye,name='facture-paye'),
    
    # facture nom paye
    path('facture_nom_paye',views.facture_nom_paye,name='facture-nom-paye'),
    
    # sav
    path('sav',views.sav,name='sav')
]
