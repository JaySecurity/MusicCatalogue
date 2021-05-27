import os

import requests
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from main_app.forms import TrackForm

from .forms import TrackForm
from .models import Album, Track

# Headers for API calls
headers = {
    'x-rapidapi-key': os.getenv('X-RAPIDAPI-KEY'),
    'x-rapidapi-host': os.getenv('X-RAPIDAPI-HOST')
    }
songkick_api = os.getenv('SONGKICK_API')

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = '/'
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        super().form_valid(form)
        login(self.request, form.instance)
        return redirect(SignUp.success_url)

class AlbumList(LoginRequiredMixin, ListView):
    model = Album
    def get_queryset(self):
      return Album.objects.filter(user = self.request.user)

class AlbumDetail(LoginRequiredMixin, DetailView):
  model = Album
  track_form = TrackForm()
  extra_context = {'track_form': track_form}

class AlbumAdd(LoginRequiredMixin, CreateView):
  model = Album
  fields = ['artist_name','title','genre', 'format']
  success_url = '/albums/'
  
  extra_context = {'headers':headers}

  def form_valid(self, form):
    album_id = None
    form.instance.user = self.request.user
    album = form.save(commit=False) 
    url = "https://theaudiodb.p.rapidapi.com/searchalbum.php"

    querystring = {"s":form.instance.artist_name,"a":form.instance.title}
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    
    if data['album'] != None:
      album_id = data['album'][0]['idAlbum']
      if 'strDescriptionEN' in data['album'][0].keys():
        album.description = data['album'][0]['strDescriptionEN']
      if 'strAlbum3DFace' in data['album'][0].keys():
        album.album_art_3d = data['album'][0]['strAlbum3DFace']
      if 'strAlbumThumbBack' in data['album'][0].keys():
        album.album_back_art = data['album'][0]['strAlbumThumbBack']
      if 'strAlbumThumb' in data['album'][0].keys():
        album.cover_art = data['album'][0]['strAlbumThumb']
      if 'strAlbumCDart' in data['album'][0].keys():
        album.cd_art = data['album'][0]['strAlbumCDart']
      if 'intYearReleased' in data['album'][0].keys():
        album.release_year = data['album'][0]['intYearReleased']
      
    album.save()
    if album_id:
      url = "https://theaudiodb.p.rapidapi.com/track.php"
      querystring = {"m":album_id}
      response = requests.get(url, headers=headers, params=querystring)
      data = response.json()
      tracks = data['track']
      for track in tracks:
        new_track = Track(name = track['strTrack'], track_no = int(track['intTrackNumber']), album = album)
        new_track.save()
    return super().form_valid(form)


class AlbumUpdate(LoginRequiredMixin, UpdateView):
  model = Album
  fields = ['title', 'artist_name', 'genre', 'format', 'description']

class AlbumDelete(LoginRequiredMixin, DeleteView):
  model=Album
  success_url = '/albums/'

def artist_page(request, album_id):
  album = Album.objects.get(id = album_id)
  url = "https://theaudiodb.p.rapidapi.com/search.php"
  querystring = {"s": album.artist_name}
  response = requests.request("GET", url, headers = headers,params=querystring)
  data = response.json()
  if 'strLabel' in data['artists'][0].keys():
    artist_label = data['artists'][0]['strLabel']
  if 'strCountry' in data['artists'][0].keys():
    artist_country = data['artists'][0]['strCountry']
  if 'strWebsite' in data['artists'][0].keys():
    artist_website = data['artists'][0]['strWebsite']
  if 'strFacebook' in data['artists'][0].keys():
    artist_facebook = data['artists'][0]['strFacebook']
  if 'strTwitter' in data['artists'][0].keys():
    artist_twitter = data['artists'][0]['strTwitter']
  if 'strMusicBrainzID' in data['artists'][0].keys():
    artist_music_brainz_id = data['artists'][0]['strMusicBrainzID']
    second_url = "https://api.songkick.com/api/3.0/artists/mbid:" + artist_music_brainz_id + "/calendar.json?apikey=" + songkick_api
    r = requests.get(second_url)
  try:
    concert = r.json()['resultsPage']['results']['event'][0]
  except:
    concert = ""
  concert_details = {}
  if concert:
    concert_details = {
      'displayName' : concert['displayName'],
      'tickets': concert['uri'],
      'start_date': concert['start']['date'],
      'start_time': concert['start']['time'],
    }

  artist = {
    'label': artist_label,
    'country': artist_country,
    'website': artist_website,
    'facebook': artist_facebook,
    'twitter': artist_twitter,
  }

  return render(request, 'main_app/artist_page.html',{
    'album': album,
    'artist': artist,
    'concert': concert_details
  })




def album_search(request, artist):
  # Lookup Artist Id
  url = f"https://www.theaudiodb.com/api/v1/json/1/search.php?s={artist}"
  response = requests.get(url)
  data = response.json()
  artistId = data['artists'][0]['idArtist']

  # Lookup Album Based on Artist ID
  url = f"https://theaudiodb.p.rapidapi.com/album.php"
  querystring = {"i":artistId}
  response = requests.get(url, headers=headers, params=querystring)
  data = response.json()
  return JsonResponse(data)

@login_required
def add_track(request, album_id):
  form = TrackForm(request.POST)
  if form.is_valid():
    new_track = form.save(commit=False)
    new_track.album_id = album_id
    new_track.save()
  return redirect('albums_detail', pk=album_id)

class EditTrack(LoginRequiredMixin, UpdateView):
  model = Track
  fields = ['track_no', 'name']  

class TrackDelete(LoginRequiredMixin, DeleteView):
  model= Track

  def get_success_url(self):
    return reverse_lazy('albums_detail', kwargs={'pk':self.kwargs['album_id']})
  