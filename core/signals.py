from .models import Profile, Follow, Favourite, Movie
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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
        

# check that a profile has a picture associated, otherwise the default one is adopted as propic
@receiver(pre_save, sender=Profile)
def check_propic(sender, instance, **kwargs):
        if not instance.propic:
            instance.propic = join('static', 'default_propic.svg')
            

@receiver(pre_save, sender=Movie)
def check_poster(sender, instance, **kwargs):
    if not instance.poster:
        instance.poster = join('static', 'default_movie_poster.svg')
        
        
# check that a profile does not follows itself
@receiver(m2m_changed, sender=Follow)
def validate_follows(sender, instance, action, pk_set, **kwargs):
    if action == 'pre_add':
        if instance.pk in pk_set:
            raise ValidationError("A profile cannot follow themselves.")
        
        
# check that the favourite movies count does not exceed the maximum
@receiver(m2m_changed, sender=Favourite)
def check_favourites_movies(sender, instance, action, pk_set, **kwargs):
    if action == 'pre_add':
        if instance.favourites.count() + len(pk_set) > 4:
            raise ValidationError("A profile can have at most 4 favourite books.")