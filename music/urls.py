from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView, name='home'),
    path('search/', SearchView, name='search'),
    path('user/search/<singer>/', UserSearchView, name='usersearch'),
    path('category/<area>/', CategoryView, name='category'),
    path('music/trending/', HotView, name='hot'),
    path('report/', ReportView, name='report'),
    path('signup/', RegisterView, name='register'),
    path('music/detail/<int:pk>/', DetailView, name='detail'),
    path('del/<int:pk>/', DelView, name='del'),
    path('reply/<int:pk>/', ReplyView, name='reply'),
]
