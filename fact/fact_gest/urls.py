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
    path('entreprise',views.entreprise,name='entreprise'),
    
    # creer une entreprise
    path('creer_entreprise/',views.creer_entreprise,name='creer-entreprise'),
    
    # modifier entreprise
    path('modifier_entreprise/<int:pk>/',views.modifier_entreprise,name='modifier-entreprise'),
    
    # supprimer entreprise
    path('supprimer_entreprise/<int:pk>/',views.supprimer_entreprise,name='supprimer-entreprise'),
    
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
