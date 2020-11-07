"""MovieMice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from app import views
#from django.views import debug

urlpatterns = [
    # get defult page back
    #path('', debug.default_urlconf),
    path('', views.home, name='home'),
    path('search_results', views.search, name='search_shows'),
    path('seasons/<show_ID>', views.seasons_list, name='seasons'),
    path('<show_ID>/season<season_num>', views.episodes_list, name='episodes'),
    path('<show_ID>/season<season_num>/episode<episode_num>/episode_details', views.episode_details, name='episode_details'),
    path('actors/<cast_ID>', views.actor_details, name='actors'),
]