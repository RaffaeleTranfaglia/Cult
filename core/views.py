from django.db.models.base import Model as Model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from .models import Movie, Profile, Log, Follow, WatchList, Favourite
from .forms import CreateMovieForm, UpdateProfileForm, MovieSearchForm, LogForm
from braces.views import GroupRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.models import Group

def home_view(request):
    # 6 most popular (viewed) movies
    popular_movies = Movie.objects.all().order_by('-views_total')[:6]
    
    # last 6 published movies
    today = timezone.now().date()
    recent_movies = Movie.objects.filter(release_date__lte=today).order_by('-release_date')[:6]
    
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
                friend_logs = Log.objects.filter(profile=friend)
                if friend_logs:
                    logs.append(friend_logs[0])
            context['friends_movies'] = sorted(logs, key=lambda x : x.date, reverse=True)[:6]
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
        form.instance.production = self.request.user.profile
        return super().form_valid(form)
    
    def get_success_url(self):
        # TODO add a temporary banner that confirms the action
        return reverse('core:movie_page', kwargs={'pk' : self.object.pk})


class MovieListView(ListView):
    model = Movie
    template_name = 'movies_list.html'
    context_object_name = 'movies'
    paginate_by = 12
    
    def get_queryset(self):
        profile = get_object_or_404(Profile, user__profile__pk=self.kwargs['pk'])
        return Movie.objects.filter(production=profile)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user__profile__pk=self.kwargs['pk'])
        return context

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_page.html'
    context_object_name = 'movie'
    
    def is_available(self):
        return self.get_object().release_date <= timezone.now().date()
    

class MovieUpdateView(GroupRequiredMixin, UpdateView):
    group_required = ['business']
    model = Movie
    template_name = 'update_movie.html'
    fields = ['title', 'poster', 'plot', 'genres', 'director', 'cast', 'runtime']
    
    def dispatch(self, request, *args, **kwargs):
        movie = self.get_object()
        user_profile = request.user.profile

        if movie.production != user_profile:
            messages.error(request, "You do not have permission to modify this movie.")
            # TODO add a temporary banner that confirms the action
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        # TODO add a temporary banner that confirms the action
        return reverse('core:movie_page', kwargs={'pk' : self.object.pk})
    

class MovieDeleteView(GroupRequiredMixin, DeleteView):
    group_required = ['business']
    model = Movie
    template_name = 'delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        movie = self.get_object()
        user_profile = request.user.profile

        if movie.production != user_profile:
            messages.error(request, "You do not have permission to delete this movie.")
            # TODO add a temporary banner that confirms the action
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Movie'
        return context
    
    def get_success_url(self):
        # TODO add a temporary banner that confirms the action
        return reverse('core:home')
    
    
def movie_search(request):
    form = MovieSearchForm()
    results = Movie.objects.all()

    if request.method == 'GET' and 'field' in request.GET:
        form = MovieSearchForm(request.GET)
        if form.is_valid():
            field = form.cleaned_data['field']
            query = form.cleaned_data['query']
            filter_args = {f"{field}__icontains": query}
            results = Movie.objects.filter(**filter_args)[:100]

    return render(request, 'movie_search.html', {'form': form, 'results': results})


class UserCreationView(CreateView):
    form_class = UserCreationForm
    template_name = 'user_create.html'
    success_url = reverse_lazy('login')


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile_page.html'


def in_group(user, group_name):
    group = Group.objects.get(name=group_name)
    if group.user_set.filter(username=user.username).exists():
        return True
    else:
        return False


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


class DiaryList(ListView):
    model = Log
    template_name = 'diary_list.html'
    context_object_name = 'logs'
    paginate_by = 24
    
    def get_queryset(self):
        profile = get_object_or_404(Profile, user__profile__pk=self.kwargs['pk'])
        return Log.objects.filter(profile=profile)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user__profile__pk=self.kwargs['pk'])
        return context
    

@login_required
def toggle_follow(request, profile_id):
    if not in_group(request.user, 'base') and not in_group(request.user, 'business'):
        return JsonResponse({'error': 'Not in the authorized group'}, status = 400)
    
    if request.method == 'POST':
        if (profile_id == request.user.profile.pk):
            return JsonResponse({'error': 'A profile cannot follow themselves.'}, status=400)
        
        follows = get_object_or_404(Profile, pk=profile_id)
        follow_relation, created = Follow.objects.get_or_create(profile=request.user.profile, follows=follows)
        
        if not created:
            follow_relation.delete()
            is_following = False
        else:
            is_following = True
        
        return JsonResponse({'is_following': is_following})
    
    return JsonResponse({'error': 'Non POST request'}, status=400)


@login_required
def toggle_watchlist(request, movie_pk):
    if not in_group(request.user, 'base') and not in_group(request.user, 'business'):
        return JsonResponse({'error': 'Not in the authorized group'}, status = 400)
    
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_pk)
        watchlist_relation, created = WatchList.objects.get_or_create(
            profile=request.user.profile, 
            movie=movie,
            defaults={'date': timezone.now()}
            )
        
        if not created:
            watchlist_relation.delete()
            in_watchlist = False
        else:
            in_watchlist = True
            
        return JsonResponse({'in_watchlist': in_watchlist})
    
    return JsonResponse({'error': 'Non POST request'}, status = 400)


@login_required
def toggle_favourite(request, movie_pk):
    if not in_group(request.user, 'base') and not in_group(request.user, 'business'):
        return JsonResponse({'error': 'Not in the authorized group'}, status = 400)
    
    movie = get_object_or_404(Movie, pk=movie_pk)
    profile = request.user.profile
    if not Log.objects.filter(profile=profile, movie=movie).exists():
        return JsonResponse({'error': 'Only logged movies can be added to favourites'}, status = 400)
    
    if request.method == 'POST':
        favourite_relation, created = Favourite.objects.get_or_create(
            profile=profile, 
            movie=movie
            )
        
        if not created:
            favourite_relation.delete()
            in_favourite = False
        else:
            if (Favourite.objects.filter(profile=profile).count() >= 5):
                favourite_relation.delete()
                return JsonResponse({'error': 'A profile can have at most 4 favourite movies.'}, status=400)
            in_favourite = True
            
        return JsonResponse({'in_favourite': in_favourite})
    
    return JsonResponse({'error': 'Non POST request'}, status = 400)


@login_required
def add_log(request, movie_pk):
    if not in_group(request.user, 'base') and not in_group(request.user, 'business'):
        #TODO add a denial message
        return redirect(reverse('core:movie_page', kwargs={'pk': movie_pk}))
    
    movie = Movie.objects.get(pk=movie_pk)
    
    if movie.release_date > timezone.now().date():
        #TODO add a denial message
        return redirect(reverse('core:movie_page', kwargs={'pk': movie_pk}))
    
    if request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
            profile = request.user.profile
            existing_log = Log.objects.filter(profile=profile, movie=movie).exists()
            log_entry = form.save(commit=False)
            log_entry.profile = profile
            log_entry.movie = movie
            if existing_log:
                log_entry.just_watched = True
            log_entry.rewatch = True if existing_log else False
            log_entry.save()
            movie.views_total += 1
            movie.save()
            return redirect(reverse('core:movie_page', kwargs={'pk': movie_pk}))
    else:
        form = LogForm()
        return render(request, 'create_log.html', {'form': form, 'movie': movie})
    
    
class LogDeleteView(GroupRequiredMixin, DeleteView):
    group_required = ['base', 'business']
    model = Log
    template_name = 'delete.html'

    def dispatch(self, request, *args, **kwargs):
        profile_who_logged = self.get_object().profile
        user_profile = request.user.profile

        if profile_who_logged != user_profile:
            messages.error(request, "You do not have permission to delete this log.")
            # TODO add a temporary banner that confirms the action
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        movie = self.get_object().movie
        movie.views_total -= 1
        movie.save()
        # Perform the actual deletion
        response = super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Log'
        return context

    def get_success_url(self):
        # TODO add a temporary banner that confirms the action
        return reverse('core:profile_page', kwargs={'pk': self.get_object().profile.pk})
    
    
class WatchListView(ListView):
    model = Movie
    template_name = 'watch_list.html'
    context_object_name = 'watchlist'
    paginate_by = 24
    
    def get_queryset(self):
        profile = get_object_or_404(Profile, user__profile__pk=self.kwargs['pk'])
        return WatchList.objects.filter(profile=profile)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user__profile__pk=self.kwargs['pk'])
        return context