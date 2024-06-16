from .models import Profile, Follow, Favourite
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# checks on the creation of new profiles
@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Exclude the 'admin' user and the staff users
        if not instance.is_superuser and not instance.is_staff:
            Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
        
        
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