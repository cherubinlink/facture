from django.shortcuts import render

# Create your views here.


def parametre(request):
    return render(request,'fact_user/parametre.html')


def profile(request):
    return render(request,'fact_user/profile.html')
