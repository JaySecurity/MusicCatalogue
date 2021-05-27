from django.forms import ModelForm, fields

from .models import Track


class TrackForm(ModelForm):
  class Meta:
    model = Track
    fields = ['track_no', 'name']
