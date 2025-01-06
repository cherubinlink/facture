from django.contrib import admin
from fact_user.models import Utilisateur,Profile

# Register your models here.

class Utilisateuradmin(admin.ModelAdmin):
    list_display = ['email','username','role']
admin.site.register(Utilisateur,Utilisateuradmin)



