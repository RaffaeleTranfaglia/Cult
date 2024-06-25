from django.contrib.auth import get_user_model
from django.db import models
from os.path import join
from django.utils import timezone

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
    views_total = models.PositiveIntegerField(default=0)
    reviews_total = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.pk} {self.title} {self.release_date} views: {self.views_total} \
            reviews: {self.reviews_total}"
            
    class Meta:
        ordering = ['-release_date']     
            
    
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    propic = models.ImageField(                             # profile picture
        upload_to='profile_pictures', 
        default=join('static', 'default_propic.svg'), 
        blank=True)
    bio = models.TextField(blank=True)                      # biography
    stars = models.ManyToManyField(                         # starred reviews
        'Review', 
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
    watchlists = models.ManyToManyField(                    # watchlisted movies
        Movie, 
        through='WatchList', 
        related_name='watchlists', 
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
        return f"{self.pk} {self.user.username}"
    
    
class Follow(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='+')
    follows = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='+')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['profile', 'follows'],
                name = 'unique_follow'
            )
        ]
    
    
class Review(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    stars_total = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-date', 'profile']
        constraints = [
            models.UniqueConstraint(
                fields = ['profile', 'movie'],
                name = 'unique_review'
            )
        ]


class Star(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['profile', 'review'],
                name = 'unique_star'
            )
        ]
    
    
class Log(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    rewatch = models.BooleanField(default=False)
    just_watched = models.BooleanField(default=True)
    date = models.DateTimeField(null=True, default=timezone.now)
    
    class Meta:
        ordering = ['-date']
    

class WatchList(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields = ['profile', 'movie'],
                name = 'unique_watchlist'
            )
        ]
    
    
class Favourite(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['pk']
        constraints = [
            models.UniqueConstraint(
                fields = ['profile', 'movie'],
                name = 'unique_favourite'
            )
        ]