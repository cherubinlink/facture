from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from fact_gest.forms import GroupForm
from fact_gest.models import Group,Company


# Create your views here.

# accueil principal
def accueil(request):
    return render(request,'fact_gest/accueil.html')

# accueil utiliateur 
def accuei_user(request):
    return render(request,'fact_gest/accueil_user.html')


# voir les informations du group
def voir_group(request):
    user = request.user
    
    # Vérifie si l'utilisateur est authentifié
    # if not user.is_authenticated:
    #     messages.error(request, 'Vous devez être connecté pour accéder à cette page.')
    #     return redirect('login')
    
    try:
        # Récupère les groupes associés au propriétaire
        groupes = Group.objects.filter(proprietaire=user)
        if not groupes.exists():
            messages.error(request, 'Aucun groupe n’est associé à votre compte.')
            return redirect('accueil')

    except Group.DoesNotExist:
        messages.error(request, 'Une erreur s’est produite. Aucun groupe trouvé.')
        return redirect('accueil')
    groupes_entreprise = Group.objects.prefetch_related('companies').filter(proprietaire=user)
    total_group = groupes.count()
    context = {
        'groupes':groupes,
        'groupes_entreprise':groupes_entreprise,
        'total_group':total_group
    }
    return render(request, 'fact_gest/group.html', context)


    

# creer un group
def creer_group(request):
    user = request.user
    
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.proprietaire = user
            group.save()
        
            messages.success(request,'la creations de votre group a ete efectuez avec success')
            return redirect('voir-group')
        else:
            messages.error(request, 'Une erreur est survenue lors de la création du groupe. Veuillez réessayer.')
    else:
        form = GroupForm()
        
    context = {
        'user':user,
        'form':form
    }

    return render(request,'fact_gest/creer_group.html',context)

# modification du group
def modifier_group(request, pk):
    
    # Récupération du groupe ou renvoi d'une erreur 404
    group = get_object_or_404(Group, id=pk)
    
    # Vérification que l'utilisateur est le propriétaire du groupe
    if group.proprietaire != request.user:
        messages.error(request, "Vous n'avez pas les droits pour modifier ce groupe.")
        return redirect('voir-group')
    
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.warning(request,'mise a jour reussie')
            return redirect('voir-group')
    else:
        form = GroupForm(instance=group)
    context = {
        'group':group,
        'form':form
    }
    return render(request,'fact_gest/modifier_group.html',context)

# supprimer un group
def supprimer_group(request, pk):
    
    # Récupération du groupe ou renvoi d'une erreur 404
    group = get_object_or_404(Group, id=pk)
    
    # Vérification que l'utilisateur est le propriétaire du groupe
    if group.proprietaire != request.user:
        messages.error(request, "Vous n'avez pas les droits pour modifier ce groupe.")
        return redirect('voir-group')
    
    if request.method == 'POST':
        group.delete()
        messages.success(request,'group supprimer avec success')
        return redirect('voir-group')
    context = {
        'group':group
    }
    return render(request,'fact_gest/supprimer_group.html',context)

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


# service apres ventes
def sav(request):
    return render(request,'fact_gest/sav.html')


