from django.db import models
from fact_user.models import Utilisateur
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.


STATUS_CHOICES = (
    ('Brouillon','Brouillon'),
    ('Envoye','Envoye'),
    ('Paye','Paye'),
    ('En attente','En attente'),
    ('Annule','Annuler')
)

class Group(models.Model):
    """
    Représente un groupe qui regroupe plusieurs entreprises.
    """
    noms = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    date_creee = models.DateTimeField(auto_now_add=True)
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='groupes')

    class Meta:
        verbose_name = 'groupe'
        verbose_name_plural = 'groupes'

    def __str__(self):
        return self.noms


class Company(models.Model):
    """
    Représente une entreprise appartenant à un groupe.
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='companies')
    noms = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    pays = models.CharField(max_length=100, null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    responsable = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='entreprise_responsable')
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='entreprises_proprietaire')

    class Meta:
        verbose_name = 'entreprise'
        verbose_name_plural = 'entreprises'

    def __str__(self):
        return self.noms


class Client(models.Model):
    """
    Représente un client d'une entreprise.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='clients')
    noms = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'

    def __str__(self):
        return self.noms


class Produit(models.Model):
    """
    Représente un produit vendu par une entreprise.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='produits')
    noms = models.CharField(max_length=100)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'produit'
        verbose_name_plural = 'produits'

    def __str__(self):
        return self.noms


class CahierDeCharges(models.Model):
    """
    Représente un cahier des charges pour un service.
    """
    titre = models.CharField(max_length=100)
    description = models.TextField()
    fichier = models.FileField(upload_to='cahiers_de_charges/', null=True, blank=True)
    categorie = models.CharField(max_length=50, null=True, blank=True)
    # Ajoutez d'autres champs pertinents au cahier des charges si nécessaire

    def __str__(self):
        return self.titre

class Service(models.Model):
    """
    Représente un service offert par une entreprise, lié à un cahier de charges.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='services')
    noms = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    cahier_de_charges = models.ForeignKey(CahierDeCharges, on_delete=models.CASCADE, related_name='services')
    tarif = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # Rendre non éditable

    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'
        
    def save(self, *args, **kwargs):
        if not self.cahier_de_charges:
            raise ValueError("Un cahier des charges est requis pour enregistrer un service.")
        self.tarif = self.calculer_tarif()
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Calculer le tarif en fonction du cahier des charges
        self.tarif = self.calculer_tarif()  # Appel à une fonction pour calculer le tarif
        super().save(*args, **kwargs)

    def calculer_tarif(self):
        # Exemple : tarif basé sur la longueur de la description
        description_length = len(self.cahier_de_charges.description) if self.cahier_de_charges.description else 0
        tarif_de_base = 50  # Tarif fixe de base
        return tarif_de_base + (description_length * 0.1)  # Exemple de calcul
    
    def clean(self):
        if Service.objects.filter(company=self.company, noms=self.noms).exclude(id=self.id).exists():
            raise ValidationError(f"Un service avec le nom '{self.noms}' existe déjà pour cette entreprise.")
        super().clean()

    def __str__(self):
        return self.noms


class Facture(models.Model):
    """
    Représente une facture pour un client d'une entreprise.
    """
   
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='factures')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='factures')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    avance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_facture = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'facture'
        verbose_name_plural = 'factures'

    def __str__(self):
        return f"{self.client} - {self.total}"


class FactureProduit(models.Model):
    """
    Représente les produits associés à une facture.
    """
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='produits_factures')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='factures')
    quantite = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'facture produit'
        verbose_name_plural = 'factures produits'


class FactureService(models.Model):
    """
    Représente les services associés à une facture.
    """
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='services_factures')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='factures')
    date_debut = models.DateField()
    date_fin = models.DateField()

    class Meta:
        verbose_name = 'facture service'
        verbose_name_plural = 'factures services'