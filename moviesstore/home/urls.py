from django.urls import path
from . import views
urlpatterns = [

    path('', views.index, name='home.index'), #routes the pge with no / to home
    path('about', views.about, name='home.about'),
]