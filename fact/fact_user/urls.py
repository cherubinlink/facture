from django.urls import path
from fact_user import views



urlpatterns = [
    
    # parametre
    path('parametre',views.parametre,name='parametre'),
    
    # profile
    path('profile',views.profile,name='profile')
]
