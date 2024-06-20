from django.contrib import admin
from .models import Profile, Review, Movie

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    exclude = ['user']

admin.site.register(Review)
admin.site.register(Movie)
