from typing import Any
from django import forms
from .models import Movie, Profile
from django.shortcuts import get_object_or_404

class CreateMovieForm(forms.ModelForm):
    description = "Publish a new Movie"
    
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'plot', 'genres', 'director', 'cast', 
                  'runtime', 'release_date']
            
            
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['propic', 'bio']
        

class MovieSearchForm(forms.Form):
    SEARCH_FIELDS = [
        ('title', 'Title'),
        ('genres', 'Genres'),
        ('director', 'Director'),
        ('cast', 'Cast')
    ]

    field = forms.ChoiceField(choices=SEARCH_FIELDS, required=True)
    query = forms.CharField(max_length=255, required=True)