from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('accounts/signup', views.SignUp.as_view(), name = 'signup'),
    path('albums/', views.AlbumList.as_view(), name = 'albums_index'),
    path('albums/add', views.AlbumAdd.as_view(), name = 'albums_add'),
    path('albums/<int:pk>/', views.AlbumDetail.as_view(), name = 'albums_detail'),
    path('albums/<int:pk>/edit', views.AlbumUpdate.as_view(), name = 'albums_update'),
    path('albums/<int:pk>/delete', views.AlbumDelete.as_view(), name = 'albums_delete'),
    path('albums/<int:album_id>/artist/', views.artist_page, name = "artist_page" ),
    path('albums/<int:album_id>/tracks/add', views.add_track, name = "add_track" ),
    path('tracks/<int:pk>/edit', views.EditTrack.as_view(), name = "edit_track" ),
    path('albums/<int:album_id>/tracks/<int:pk>/delete', views.TrackDelete.as_view(), name = "delete_track" ),
    path('albums/search/<str:artist>/', views.album_search, name = "artist_search" ),
]
