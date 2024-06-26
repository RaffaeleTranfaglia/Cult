from django import template
from core.models import Log

register = template.Library()

'''
Return the last logged movies for the given profile.
'''
@register.filter(name='last_logs')
def last_logs(profile, n_logs):
    return Log.objects.filter(profile=profile)[:n_logs]

'''
Return True if the given profile has at least one log of the given movie.
'''
@register.filter(name='has_logged')
def has_logged(profile, movie):
    return Log.objects.filter(profile=profile, movie=movie).exists()


'''
Return the more recent log related to the given movie, if it exists.
'''
@register.filter(name='get_last_log')
def get_last_log(profile, movie):
    if has_logged(profile, movie):
        return Log.objects.filter(profile=profile, movie=movie)[0]
    return None