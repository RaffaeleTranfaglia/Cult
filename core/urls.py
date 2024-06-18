from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('', home_view, name='home'),
    path('movie/<pk>/', MovieDetail.as_view(), name='moviepage'),
    path('profile/<pk>', ProfileDetail.as_view(), name='profilepage')
]
