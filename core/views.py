from typing import Any
from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Movie, Profile

def home_view(request):
    # 10 most popular (viewed) movies
    popular_movies = Movie.objects.all().order_by('-views_total')[:10]
    
    # last 10 published movies (movies db is ordered by release date in descending order)
    recent_movies = Movie.objects.all()[:10]
    
    context = { 
        'pagename' : 'Home',
        'popular_movies': popular_movies, 
        'recent_movies': recent_movies, 
        'friends_movies': None
    }

    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        if user_profile:
            logs = []
            following_profiles = user_profile.follows.all()
            for friend in following_profiles:
                # friend's last movie logged (logs db is ordered by date in descending order)
                logs.append(friend.logs.all()[0])
            context['friends_movies'] = sorted(logs, key=lambda x : x.date, reverse=True)[:10]
    
    return render(request, template_name='home.html', context=context)