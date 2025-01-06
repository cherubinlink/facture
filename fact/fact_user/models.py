from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.


ROLE_UTILISATEUR = (
    ('Proprietaire', 'Propriétaire'),
    ('Manager', 'Manager'),
)


class Utilisateur(AbstractUser):
    """
    Représente le modèle utilisateur personnalisé avec un rôle spécifique.
    """
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)  # Ajout de `unique=True`
    role = models.CharField(max_length=50, choices=ROLE_UTILISATEUR, default='Manager')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Profile(models.Model):
    """
    Profil utilisateur étendu avec des champs supplémentaires.
    """
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='profile')
    noms = models.CharField(max_length=100, null=True, blank=True)
    prenoms = models.CharField(max_length=100, null=True, blank=True)
    ville = models.CharField(max_length=100, null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - Profil'


@receiver(post_save, sender=Utilisateur)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Crée ou met à jour un profil utilisateur lors de la sauvegarde d'un utilisateur.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

