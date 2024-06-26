from .models import Profile, Movie, Log, WatchList
from django.db.models.signals import post_save, m2m_changed, pre_save
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