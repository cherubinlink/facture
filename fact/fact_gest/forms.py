from django import forms
from fact_gest.models import Group,Company,Client,Produit



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
                'placeholder': 'Nom'
            }),
              'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'email'
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Adresse'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'telephone'
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

    