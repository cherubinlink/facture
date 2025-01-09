from django import forms
from fact_gest.models import Group,Company,Client



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
        if email:
            qs = Client.objects.filter(email=email).exclude(id=self.instance.id)  # Exclure l'instance actuelle
            if qs.exists():
                raise forms.ValidationError("Un client avec cet email existe déjà.")
        return email