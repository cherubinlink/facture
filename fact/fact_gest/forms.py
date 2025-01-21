from django import forms
from fact_gest.models import Group,Company,Client,Produit,Service,Facture,Client,FactureProduit



class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['noms', 'description']
        widgets = {
            'noms': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nom du groupe'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Description du groupe (facultatif)'
            }),
        }
        
    def clean_noms(self):
        noms = self.cleaned_data.get('noms')
        
        # Vérifier uniquement lors de la création (si l'instance n'a pas encore de pk)
        if not self.instance.pk:  # Si l'instance n'a pas de pk, c'est une création
            if Group.objects.filter(noms=noms).exists():
                raise forms.ValidationError("Un groupe existe déjà avec ce nom.")
        
        return noms
    

class CompanyForm(forms.ModelForm):
    
    class Meta:
        model = Company
        fields = ['noms', 'adresse', 'pays', 'ville', 'description']
        exclude = ['proprietaire', 'groupe', 'responsable']
        widgets = {
            'noms': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nom de l\'entreprise'
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Adresse'
            }),
            'pays': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nom du pays'
            }),
            'ville': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nom de la ville'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Description de l entreprise (facultatif)'
            }),
        }
        
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['noms','email','adresse','telephone']
        widgets = {
            'noms': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nom obligatoire'
            }),
              'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'email pas obligatoire'
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Adresse pas obligatoire'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'telephone pas obligatoire'
            }),
          
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        company = self.cleaned_data.get('company')  # Récupérer l'entreprise
        
        if email and company:
            qs = Client.objects.filter(email=email, company=company)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Cet email est déjà utilisé pour un autre client de cette entreprise.")
        
        return email

class ProduitForm(forms.ModelForm):
    
    class Meta:
        model = Produit
        fields = ['noms','prix_achat','prix_vente','stock']
        widgets = {
            'noms': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nom'
            }),
            'prix_achat': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'prix d/achat'
            }),
            'prix_vente': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'prix vente'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'stock'
            }),
        }
        

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['noms','description','actif']
        widgets = {
            'noms': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nom du service'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'description du service'
            }),
            'actif': forms.CheckboxInput(attrs={
                'class': 'form-control', 
                'placeholder': 'actif'
            }),
        }


class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['avance', 'total', 'status']
        widgets = {
            'avance': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Avance facture'
            }),
            'total': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Total facture'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.pk and not hasattr(self.instance, 'company'):
            raise forms.ValidationError("Une entreprise doit être associée à cette facture.")
        return cleaned_data
        
class FactureProduitForm(forms.ModelForm):
    
    class Meta:
        model = FactureProduit
        fields = ['produit','quantite']
        widgets = {
            'produit': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nom du produits'
            }),
             'quantite': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'quantite'
            }),
        }

    