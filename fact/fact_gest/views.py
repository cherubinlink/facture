from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from fact_gest.forms import GroupForm,CompanyForm,ClientForm,ProduitForm
from fact_gest.models import Group,Company,Produit,Client,Facture,Service
import logging

logger = logging.getLogger(__name__)

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


# detail group
def detail_group(request, group_id):
    
    group = get_object_or_404(Group, id=group_id)
    entreprise = group.companies.all()
    groupes_entreprise = Group.objects.prefetch_related('companies').filter(proprietaire=request.user)
    
    
    context = {
        'group':group,
        'entreprise':entreprise,
        'groupes_entreprise':groupes_entreprise
    }
    return render(request,'fact_gest/detail_group.html',context)


    

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
def entreprise(request, pk):
    user = request.user
    entreprise = get_object_or_404(Company, id=pk)
    
    clients = Client.objects.filter(company=entreprise)
    produits = Produit.objects.filter(company=entreprise)
    services = Service.objects.filter(company=entreprise)
    factures = Facture.objects.filter(company=entreprise)    
    context = {
        'user':user,
        'entreprise':entreprise,
        'clients':clients,
        'produits':produits,
        'services':services,
        'factures':factures
    }
    return render(request,'fact_gest/entreprise.html',context)


# creer une entreprise
def creer_entreprise(request):
    
    user = request.user
    
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.proprietaire = user
            
            group = Group.objects.filter(proprietaire=user).first()
            if group:
                company.group = group
            
            company.save()
            messages.success(request,'votre entreprise a ete creer avec success')
            return redirect('detail-group', group_id=company.group.id)
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = CompanyForm()
    context = {
        'form':form
    } 
    return render(request,'fact_gest/creer_entreprise.html',context)


# modification une entreprise
def modifier_entreprise(request, pk):
    # Récupération de l'entreprise ou renvoi d'une erreur 404
    company = get_object_or_404(Company, id=pk)
    
    # Vérification que l'utilisateur est le propriétaire de l'entreprise
    if company.proprietaire != request.user:
        messages.error(request, "Vous n'avez pas les droits pour modifier cette entreprise.")
        return redirect('voir-group')
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mise à jour réussie.')
            return redirect('detail-group', group_id=company.group.id)
    else:
        form = CompanyForm(instance=company)
    
    context = {
        'company': company,
        'form': form
    }
    
    return render(request, 'fact_gest/modifier_entreprise.html', context)

# supprimer une entreprise
def supprimer_entreprise(request, pk):
    
    # Récupération du groupe ou renvoi d'une erreur 404
    company = get_object_or_404(Company, id=pk)
    
    # Vérification que l'utilisateur est le propriétaire du groupe
    if company.proprietaire != request.user:
        messages.error(request, "Vous n'avez pas les droits pour modifier ce groupe.")
        return redirect('voir-group')
    
    if request.method == 'POST':
        company.delete()
        messages.success(request,'group supprimer avec success')
        return redirect('detail-group', group_id=company.group.id)
    context = {
        'company':company
    }
    return render(request,'fact_gest/supprimer_entreprise.html',context)



# produits
def produit(request, entreprise_id):
    
    entreprise = get_object_or_404(Company, id=entreprise_id)
    
    seaech_query = request.GET.get('search', '').strip()
    
    if seaech_query:
        produits = Produit.objects.filter(company=entreprise, noms__icontains=seaech_query).order_by('-id')
    else:
        produits = Produit.objects.filter(company=entreprise).order_by('-id')
    
    produit_count = produits.count()
    
    context = {
        'entreprise':entreprise,
        'produits':produits,
        'produit_count':produit_count
    }
    return render(request,'fact_gest/produit.html',context)

# ajouter produit
def ajouter_produit(request, entreprise_id):
    
    company = get_object_or_404(Company, id=entreprise_id)
    
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            produit = form.save(commit=False)
            produit.company = company
            produit.save()
            
            messages.success(request,'produit ajouter avec success')
            return redirect('produit', entreprise_id=entreprise_id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ProduitForm()
    context = {
        'company':company,
        'form':form
    }
    return render(request,'fact_gest/ajouter_produit.html',context)

# modifier produit
def modifier_produit(request, produit_id):
    
    produit = get_object_or_404(Produit, id=produit_id)
    logger.info(f"produit recupere : {produit.noms}")
    
    if request.method == 'POST':
        logger.info("requete POST detectee")
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            logger.info("formulaire valide")
            form.save()
            messages.success(request, 'Mise à jour réussie avec succès.')
            return redirect('produit', entreprise_id=produit.company.id)
        else:
            logger.warning("Formulaire invalide.")
            logger.warning(form.errors)  # Affiche les erreurs du formulaire dans les journaux
            messages.error(request, 'Veuillez vérifier vos informations avant de soumettre.')
    else:
        form = ProduitForm(instance=produit)
    context = {
        'form':form,
        'produit':produit
    }
    return render(request,'fact_gest/modifier_produit.html',context)

# supprimer produit
def supprimer_produit(request, entreprise_id):
    
    entreprise = get_object_or_404(Company, id=entreprise_id)
    
    if request.method == 'POST':
        produit_ids = request.POST.getlist('produits')
        if produit_ids:
            Produit.objects.filter(id__in=produit_ids, company=entreprise).delete()
            messages.success(request, 'produit supprimés avec succès!')
        else:
            messages.warning(request, 'Aucun produit sélectionné.')

        return redirect('produit', entreprise_id=entreprise_id)  # Redirige vers la page de clients
        # Récupérer les clients de l'entreprise spécifiée pour l'affichage
    produits = Client.objects.filter(company=entreprise).order_by('-id')
    produit_count = produits.count()

    context = {
        'entreprise': entreprise,
        'produits': produits,
        'produit_count': produit_count
    }
    return render(request, 'fact_gest/supprimer_produit.html', context)

# services
def service(request):
    return render(request,'fact_gest/service.html')


# clients
def client(request, entreprise_id):
    
    entreprise = get_object_or_404(Company, id=entreprise_id)
    
    # Récupérer le paramètre de recherche de la requête
    search_query = request.GET.get('search', '').strip()

    # Filtrer les clients en fonction de la recherche
    if search_query:
        clients = Client.objects.filter(company=entreprise, noms__icontains=search_query).order_by('-id')
    else:
        clients = Client.objects.filter(company=entreprise).order_by('-id')
    
   
    client_count = clients.count()
    
    context = {
        'entreprise':entreprise,
        'clients':clients,
        'client_count': client_count,
        'search_query': search_query,
    }
    return render(request,'fact_gest/client.html',context)

# ajouter un client
def ajouter_client(request, entreprise_id):
    
    company = get_object_or_404(Company, id=entreprise_id)
    
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.company = company
            client.save()
            
            messages.success(request, 'client ajouter avec success')
            return redirect('client', entreprise_id=entreprise_id)
        else:
            # Afficher les erreurs de validation
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ClientForm()
    context = {
        'company':company,
        'form':form
    }
    return render(request,'fact_gest/ajouter_client.html',context)

# modifier un client
def modifier_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    logger.info(f"Client récupéré : {client.noms}")

    if request.method == 'POST':
        logger.info("Requête POST détectée.")
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            logger.info("Formulaire valide.")
            form.save()
            messages.success(request, 'Mise à jour réussie avec succès.')
            return redirect('client', entreprise_id=client.company.id)
        else:
            logger.warning("Formulaire invalide.")
            logger.warning(form.errors)  # Affiche les erreurs du formulaire dans les journaux
            messages.error(request, 'Veuillez vérifier vos informations avant de soumettre.')
    else:
        form = ClientForm(instance=client)

    context = {
        'form': form,
        'client': client
    }
    return render(request, 'fact_gest/modifier_client.html', context)

# suppresion des clients
def supprimer_clients(request, entreprise_id):
    # Récupérer l'entreprise concernée
    entreprise = get_object_or_404(Company, id=entreprise_id)

    if request.method == 'POST':
        client_ids = request.POST.getlist('clients')  # Récupère les IDs des clients à supprimer
        if client_ids:
            # Supprime les clients qui appartiennent à l'entreprise spécifiée
            Client.objects.filter(id__in=client_ids, company=entreprise).delete()
            messages.success(request, 'Clients supprimés avec succès!')
        else:
            messages.warning(request, 'Aucun client sélectionné.')

        return redirect('client', entreprise_id=entreprise_id)  # Redirige vers la page de clients

    # Récupérer les clients de l'entreprise spécifiée pour l'affichage
    clients = Client.objects.filter(company=entreprise).order_by('-id')
    client_count = clients.count()

    context = {
        'entreprise': entreprise,
        'clients': clients,
        'client_count': client_count
    }
    return render(request, 'fact_gest/supprimer_clients.html', context)

# detail client
def detail_client(request):
    return render(request, 'fact_gest/detail_client.html')
    
    

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


