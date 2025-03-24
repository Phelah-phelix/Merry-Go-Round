from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pick/', views.pick_number, name='pick_number'),
    path('results/', views.results, name='results'),
    path('clear/', views.clear_results, name='clear_results'),
    path('save/', views.save_results, name='save_results'),
]