
from datetime import datetime
from typing import SupportsFloat
from django.http import request
from django.shortcuts import render
from django.http import HttpRequest
from app import fetch

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    stuff = fetch.fetch.get_onTV()       
    tvShowPosters = stuff[0]
    tvShowIDs = stuff[1]
    tvShowTitle = stuff[2]
    video = ""

    posterId = request.POST.get('onTVId')
    if posterId == None:
        posterId = " "
    else:
        stuff = fetch.fetch.get_videoFromId(posterId)       
        video = stuff[0]

    return render(
        request,
        'app/onTV.html',
        {
            'title':'TV Shows',
            'tvVideo':video,
            'showDetails': zip(tvShowPosters,tvShowIDs,tvShowTitle),
        }
    )

def search(request):
    assert isinstance(request, HttpRequest)

    searchTerm = request.POST.get('searchTerm')
    if searchTerm == "":
        searchTerm = " "
    
    stuff = fetch.fetch.get_shows(searchTerm)       
    tvShowPosters = stuff[0]
    tvShowIDs = stuff[1]
    tvShowTitle = stuff[2]

    return render(
        request,
        'app/layout.html',
        {
            'title':'TV Shows',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'showDetails': zip(tvShowPosters,tvShowIDs,tvShowTitle),
        }
    )

def seasons_list(request, show_ID):
    assert isinstance(request, HttpRequest)

    stuff = fetch.fetch.get_seasons(show_ID)
    seasonPosters = stuff[0]
    seasonTitles = stuff[1]
    seasonNums = stuff[2]
    seasonOverview = stuff[3]

    return render(
        request, 
        'app/seasons.html',
        {
            'title': 'Seasons',
            'message': 'Your momma calls my momma a nice name',
            'year': datetime.now().year,
            'seasonDetails': zip(seasonPosters, seasonTitles, seasonNums, seasonOverview),
        }
    )

def episodes_list(request, season_num):
    assert isinstance(request, HttpRequest)

    stuff = fetch.fetch.get_episodes(season_num)
    ep_names = stuff[0]
    ep_IDs = stuff[1]
    ep_posters = stuff[2]

    return render(
        request,
        'app/episodes.html',
        {
            'title': 'Episodes',
            'message': 'Description for the page',
            'year': datetime.now().year,
            'ep_details': zip(ep_names, ep_IDs, ep_posters),
        }
    )

def series_details(request):
    assert isinstance(request, HttpRequest)

    creatorStuffs, tvShowDetails, tvShowPoster, castDetails, imagesPaths = fetch.fetch.get_season_details()  
    creators = creatorStuffs[0]
    creatorPics = creatorStuffs[1]
    
    if castDetails==[]:
        casts = ""
        castPics=""
        castIDs=""
    else:    
        casts = castDetails[0]
        castPics = castDetails[1]
        castIDs= castDetails[2]

    return render(
        request,
        'app/tvshow_masterdetails.html',
        {
            'showCreators': zip(creators,creatorPics),
            'showCasts': zip(casts,castPics,castIDs),
            'extraImages': imagesPaths,
            'tvShowPoster': tvShowPoster,
            'tvShowID': tvShowDetails[0],
            'tvShowName': tvShowDetails[1],
            'tvShowOverview': tvShowDetails[2],
            'tvShowRating': tvShowDetails[3],
            'tvShowTotalSeasons': tvShowDetails[4],
            'tvShowTotalEpisodes':tvShowDetails[5],
        }
    )