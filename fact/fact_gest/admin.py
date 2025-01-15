from django.contrib import admin
from fact_gest.models import Group,Company,Client,Produit,Service,Facture,FactureProduit

# Register your models here.


class GroupAdmin(admin.ModelAdmin):
    list_display = ['noms','description','date_creee','proprietaire']
admin.site.register(Group,GroupAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['group','noms','adresse','pays','ville','responsable','proprietaire']
admin.site.register(Company, CompanyAdmin)

class ProduitAdmin(admin.ModelAdmin):
    list_display = ['company','noms','prix_achat','prix_vente','stock']
admin.site.register(Produit,ProduitAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['company','noms','description','actif']
admin.site.register(Service,ServiceAdmin)

class FactureAdmin(admin.ModelAdmin):
    list_display = ['company','client','total','avance','date_facture','status']
admin.site.register(Facture,FactureAdmin)

class FactureproduitAdmin(admin.ModelAdmin):
    list_display = ['facture','produit','quantite']
admin.site.register(FactureProduit,FactureproduitAdmin)



class ClientAdmin(admin.ModelAdmin):
    list_display = ['noms','email','adresse','telephone','company']
admin.site.register(Client, ClientAdmin)