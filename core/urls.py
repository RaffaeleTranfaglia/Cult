from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'core'

urlpatterns = [
    path('', home_view, name='home'),
    path('movie/create/', MovieCreateView.as_view(), name='create_movie'),
    path('movie/<pk>/', MovieDetailView.as_view(), name='movie_page'),
    path('movie/<pk>/update/', MovieUpdateView.as_view(), name='update_movie'),
    path('movie/<pk>/delete/', MovieDeleteView.as_view(), name='delete_movie'),
    path('register/', UserCreationView.as_view(), name='register'),
    path("login/", auth_views.LoginView.as_view(), name="login"), 
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('profile/<pk>/', ProfileDetailView.as_view(), name='profile_page')
]
