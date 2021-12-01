from django.urls import path
from calculator import views

# gets the view for this page from the app/views.py folder
# connects to the project/urls.py

app_name = 'calculator'
urlpatterns = [
    path('', views.calculator, name='calculator'),
    path('about/', views.about, name='about')
]
