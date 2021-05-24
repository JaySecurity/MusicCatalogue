from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .models import Album, Track

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

class AlbumAdd(LoginRequiredMixin, CreateView):
  model = Album
  fields = ['title', 'artist_name', 'genre', 'format']
  success_url = '/albums/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    # Add Login here to make api request for tracks and album art
    return super().form_valid(form)
  
