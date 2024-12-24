from django.shortcuts import render

# Create your views here.


def accueil(request):
    return render(request,'fact_gest/accueil.html')


def accuei_user(request):
    return render(request,'fact_gest/accueil_user.html')


def produit(request):
    return render(request,'fact_gest/produit.html')
