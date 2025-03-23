from django.urls import path
from . import views  # Import views from the current app

# Define the urlpatterns list
urlpatterns = [
    path('', views.home, name='home'),  # Home page URL
    path('pick/', views.pick_number, name='pick_number'),  # URL for picking a number
    path('results/', views.results, name='results'),  # URL for viewing results
]