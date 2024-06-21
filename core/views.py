from typing import Any
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Movie, Profile
from .forms import CreateMovieForm, UpdateProfileForm
from braces.views import GroupRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def home_view(request):
    # 10 most popular (viewed) movies
    popular_movies = Movie.objects.all().order_by('-views_total')[:10]
    
    # last 10 published movies (movies db is ordered by release date in descending order)
    recent_movies = Movie.objects.all()[:10]
    
    context = { 
        'popular_movies': popular_movies, 
        'recent_movies': recent_movies, 
    }

    if request.user.is_authenticated:
        try:
            user_profile = Profile.objects.get(user=request.user)
            logs = []
            following_profiles = user_profile.follows.all()
            for friend in following_profiles:
                # friend's last movie logged (logs db is ordered by date in descending order)
                logs.append(friend.logs.all()[0])
            context['friends_movies'] = sorted(logs, key=lambda x : x.date, reverse=True)[:10]
        except Profile.DoesNotExist:
            context['friends_movies'] = None
            
    #TODO insert recommended movies
    
    return render(request, template_name='home.html', context=context)


class MovieCreateView(GroupRequiredMixin, CreateView):
    group_required = ['business']
    model = Movie
    form_class = CreateMovieForm
    template_name = 'create_movie.html'
    
    def form_valid(self, form):
        form.instance.productions = self.request.profile
        return super().form_valid(form)
    
    def get_success_url(self):
        # TODO add a temporary banner that confirms the action
        return reverse('core:movie_page', kwargs={'pk' : self.object.pk})


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_page.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['pagename'] = self.object.title
        return context
    

class MovieUpdateView(GroupRequiredMixin, UpdateView):
    group_required = ['business']
    model = Movie
    template_name = 'update_movie.html'
    fields = ['title', 'poster', 'plot', 'genres', 'director', 'cast', 'runtime']
    
    def get_success_url(self):
        # TODO add a temporary banner that confirms the action
        return reverse('core:movie_page', kwargs={'pk' : self.object.pk})
    

class MovieDeleteView(GroupRequiredMixin, DeleteView):
    group_required = ['business']
    model = Movie
    template_name = 'delete_movie.html'
    
    def dispatch(self, request, *args, **kwargs):
        movie = self.get_object()
        user_profile = request.user.profile

        if movie.production != user_profile:
            messages.error(request, "You do not have permission to delete this movie.")
            # TODO add a temporary banner that confirms the action
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        # TODO add a temporary banner that confirms the action
        return reverse('core:home')


class UserCreationView(CreateView):
    form_class = UserCreationForm
    template_name = 'user_create.html'
    success_url = reverse_lazy('login')


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile_page.html'
    

@login_required
def update_profile_view(request, pk):
    if pk != str(request.user.profile.pk):
        # TODO add a temporary banner that confirms the action
        return redirect('core:home')
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('core:profile_page', kwargs={'pk' : request.user.profile.pk}))
    else:
        form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'update_profile.html', {'form': form})