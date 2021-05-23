from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('accounts/signup', views.SignUp.as_view(), name = 'signup'),
    path('albums/', views.AlbumList.as_view(), name = 'albums_index'),
]