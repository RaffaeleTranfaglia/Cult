from django.contrib.auth import get_user_model
from django.db import models
from os.path import join

#TODO search about Meta class (constraints on foreign keys)
#TODO comments

class Movie(models.Model):
    title = models.CharField(max_length=50)
    poster = models.ImageField(
        upload_to='movie_posters',
        default=join('static', 'default_movie_poster.svg'),
        blank=True
    )
    plot = models.TextField()
    genres = models.CharField(max_length=50)
    director = models.CharField(max_length=50)
    cast = models.CharField(max_length=150)
    runtime = models.DurationField()
    release_date = models.DateField()
    production = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='production')
    views_total = models.PositiveIntegerField()
    reviews_total = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.pk} {self.title} {self.release_date} views: {self.views_total} 
            reviews: {self.reviews_total}"
            
            
    
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    propic = models.ImageField(                             # profile picture
        upload_to='profile_pictures', 
        default=join('static', 'default_propic.svg'), 
        blank=True)
    bio = models.TextField(blank=True)                      # biography
    stars = models.ManyToManyField(                         # starred reviews
        Review, 
        through='Star', 
        related_name='stars', 
        blank=True)
    reviews = models.ManyToManyField(                       # movies reviews
        Movie, 
        through='Review', 
        related_name='reviews', 
        blank=True)
    logs = models.ManyToManyField(                          # logged movies
        Movie, 
        through='Log', 
        related_name='logs', 
        blank=True)
    whatchlist = models.ManyToManyField(                    # watchlisted movies
        Movie, 
        through='WatchList', 
        related_name='watchlist', 
        blank=True)
    favourites = models.ManyToManyField(                    # favourites movies
        Movie,
        through='Favourite',
        related_name='favourites',
        blank=True
    )
    follows = models.ManyToManyField(                       # followed profiles
        'self', 
        through='Follow', 
        related_name='followers', 
        symmetrical=False, 
        blank=True)
    
    def __str__(self):
        return f"{self.pk} {self.username}"