from django import forms
from fact_gest.models import Group,Company



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