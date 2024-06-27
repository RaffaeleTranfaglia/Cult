from .models import Profile, Movie, Log, WatchList, Review, Star
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from os.path import join
from django.contrib.auth.models import Group

# checks on the creation of new profiles and their update
@receiver(post_save, sender=get_user_model())
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Exclude the staff users and the 'admin' users
    base_group = Group.objects.get(name='base')
    business_group = Group.objects.get(name='business')
    if instance.is_staff or instance.is_superuser:
        try:
            profile = Profile.objects.get(user=instance)
            profile.delete()
            base_group.user_set.delete(instance)
            business_group.user_set.delete(instance)
            return
        except Profile.DoesNotExist:
            return
    if created:
        Profile.objects.create(user=instance)
        base_group.user_set.add(instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
        

# check that a profile has a picture associated, otherwise the default one is adopted
@receiver(pre_save, sender=Profile)
def check_propic(sender, instance, **kwargs):
        if not instance.propic:
            instance.propic = join('static', 'default_propic.svg')
            

# check that a movie has a poster associated, otherwise the default one is adopted
@receiver(pre_save, sender=Movie)
def check_poster(sender, instance, **kwargs):
    if not instance.poster:
        instance.poster = join('static', 'default_movie_poster.svg')
        

# Ensure that when a movie is logged, it is removed from watchlist
@receiver(post_save, sender=Log)
def synchronize_watchlist(sender, instance, **kwargs):
    movie = instance.movie
    profile = instance.profile
    
    if (WatchList.objects.filter(profile=profile, movie=movie).exists()):
        watchlist_instance = WatchList.objects.get(profile=profile, movie=movie)
        watchlist_instance.delete()
        

# When a log is added or deleted, the views of the movie are updated
@receiver(post_save, sender=Log)
def increment_views(sender, instance, **kwargs):
    movie = instance.movie
    movie.views_total += 1
    movie.save()

@receiver(post_delete, sender=Log)
def decrement_views(sender, instance, **kwargs):
    movie = instance.movie
    movie.views_total -= 1
    movie.save()
    
    
# When a review is added or deleted, the reviews number of the movie is updated
@receiver(post_save, sender=Review)
def increment_reviews(sender, instance, **kwargs):
    movie = instance.movie
    movie.reviews_total += 1
    movie.save()

@receiver(post_delete, sender=Review)
def decrement_reviews(sender, instance, **kwargs):
    movie = instance.movie
    movie.reviews_total -= 1
    movie.save()
    
    
# When a star is added or deleted, the stars number of the review is updated
@receiver(post_save, sender=Star)
def increment_stars(sender, instance, **kwargs):
    review = instance.review
    review.stars_total += 1
    review.save()
    
@receiver(post_delete, sender=Star)
def decrement_stars(sender, instance, **kwargs):
    review = instance.review
    review.stars_total -= 1
    review.save()