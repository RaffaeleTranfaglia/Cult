from django import forms
from .models import Movie, Profile

class CreateMovieForm(forms.ModelForm):
    description = "Publish a new Movie"
    
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'plot', 'genres', 'director', 'cast', 
                  'runtime', 'release_date', 'production']
        
    def __init__(self, profile, *args, **kwargs):
        super(CreateMovieForm, self).__init__(*args, **kwargs)
        try:
            # Set the field to be disabled (not editable)
            self.fields['production'].disabled = True
            self.fields['production'] = profile
        except:
            self.add_error('production', 'Error on profile')
            
            
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['propic', 'bio']
