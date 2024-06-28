from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'core'

urlpatterns = [
    path('', home_view, name='home'),
    
    path('movie/create/', MovieCreateView.as_view(), name='create_movie'),
    path('movie/search/', movie_search, name='movie_search'),
    path('movie/toggle_watchlist/<int:movie_pk>/', toggle_watchlist, name='toggle_watchlist'),
    path('movie/toggle_favourite/<int:movie_pk>/', toggle_favourite, name='toggle_favourite'),
    path('movie/<pk>/', MovieDetailView.as_view(), name='movie_page'),
    path('movie/<pk>/update/', MovieUpdateView.as_view(), name='update_movie'),
    path('movie/<pk>/delete/', MovieDeleteView.as_view(), name='delete_movie'),
    path('movie/<pk>/reviews/', MovieReviewListView.as_view(), name='movie_review_list'),
    path('movie/<pk>/production', MovieListView.as_view(), name='production'),
    
    path('register/', UserCreationView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name="login"), 
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    
    path('profile/search/', profile_search, name='profile_search'),
    path('profile/toggle_follow/<int:profile_id>/', toggle_follow, name='toggle_follow'),
    path('profile/<pk>/', ProfileDetailView.as_view(), name='profile_page'),
    path('profile/<pk>/update/', update_profile_view, name='update_profile'),
    path('profile/<pk>/diary/', DiaryList.as_view(), name='diary'),
    path('profile/<pk>/followings/', FollowingView.as_view(), name='following_list'),
    path('profile/<pk>/followers/', FollowersView.as_view(), name='followers_list'),
    path('profile/<pk>/reviews/', ProfileReviewListView.as_view(), name='profile_review_list'),
    
    path('log/create/<movie_pk>/', add_log, name='create_log'),
    path('log/delete/<int:pk>/', LogDeleteView.as_view(), name='delete_log'),
    
    path('watchlist/<int:pk>/', WatchListView.as_view(), name='watchlist'),
    
    path('review/create/<int:movie_pk>/', create_review, name='create_review'),
    path('review/delete/<int:pk>/', ReviewDeleteView.as_view(), name='delete_review'),
    path('review/toggle_star/<int:review_pk>/', toggle_star, name='toggle_star')
]
