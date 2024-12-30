from django.shortcuts import render

# Create your views here.

# accueil principal
def accueil(request):
    return render(request,'fact_gest/accueil.html')

# accueil utiliateur 
def accuei_user(request):
    return render(request,'fact_gest/accueil_user.html')

# entreprise
def entreprise(request):
    return render(request,'fact_gest/entreprise.html')

# produits
def produit(request):
    return render(request,'fact_gest/produit.html')

# services
def service(request):
    return render(request,'fact_gest/service.html')


# clients
def client(request):
    return render(request,'fact_gest/client.html')

# facture
def facture(request):
    return render(request,'fact_gest/facture.html')

# facture paye
def facture_paye(request):
    return render(request,'fact_gest/facture_paye.html')


# facture nom paye
def facture_nom_paye(request):
    return render(request,'fact_gest/facture_nom_paye.html')


