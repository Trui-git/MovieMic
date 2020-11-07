
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
    tvShowTitles = stuff[2]


    stuff = fetch.fetch.get_search_result_details(tvShowIDs)
    tvShowOverviews = stuff[0]
    tvShowHomepages = stuff[1]
    tvShowBackdrops = stuff[2]

    return render(
        request,
        'app/layout.html',
        {
            'title':'TV Shows',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'showDetails': zip(tvShowPosters, tvShowIDs, tvShowTitles, tvShowOverviews, tvShowHomepages, tvShowBackdrops),
        }
    )

def seasons_list(request, show_ID):
    assert isinstance(request, HttpRequest)

    stuff = fetch.fetch.get_seasons(show_ID)
    seasonPosters = stuff[0]
    seasonTitles = stuff[1]
    seasonNums = stuff[2]
    seasonOverview = stuff[3]

    seasonBackDrop = []
    for num in seasonNums:
        backdrop = fetch.fetch.get_season_backdrop(num)
        seasonBackDrop.append(backdrop)

    return render(
        request, 
        'app/seasons.html',
        {
            'title':'TV Shows',
            'showID': show_ID,
            'year': datetime.now().year,
            'seasonDetails': zip(seasonPosters, seasonTitles, seasonNums, seasonOverview, seasonBackDrop),
        }
    )

def episodes_list(request, show_ID, season_num):
    assert isinstance(request, HttpRequest)

    totalSeason = fetch.fetch.get_max_seasons(show_ID)
    # prevent user keying season number from url greater than total season
    if int(season_num) > int(totalSeason):
        season_num = str(totalSeason)
    
    stuff = fetch.fetch.get_episodes(show_ID, season_num)
    ep_names = stuff[0]
    ep_IDs = stuff[1]
    ep_posters = stuff[2]

    creatorStuffs, tvShowDetails, tvShowPoster, castDetails, imagesPaths, video = fetch.fetch.get_season_details(show_ID, season_num)
    creators = creatorStuffs[0]
    creatorPics = creatorStuffs[1]
    episodeRunTime = tvShowDetails[6]
    if len(episodeRunTime) == 0 :
        episodeRunTime = "N/A "  
    else:
        episodeRunTime = tvShowDetails[6][0] 

    if castDetails == []:
        casts = ""
        castPics = ""
        castIDs = ""
        castCharacters = ""
    else:    
        casts = castDetails[0]
        castPics = castDetails[1]
        castIDs = castDetails[2]
        castCharacters = castDetails[3]

    return render(
        request,
        'app/episodes.html',
        {
            'title':'TV Shows',
            'showCreators': zip(creators, creatorPics),
            'showCasts': zip(casts, castPics, castIDs, castCharacters),
            'extraImages': imagesPaths,
            'tvShowPoster': tvShowPoster,
            'tvShowID': tvShowDetails[0],
            'tvShowName': tvShowDetails[1],
            'tvShowOverview': tvShowDetails[8],
            'tvShowRating': tvShowDetails[3],
            'tvShowTotalSeasons': tvShowDetails[4],
            'tvShowTotalEpisodes':tvShowDetails[5],
            'tvShowRunTime':episodeRunTime,
            'tvShowFirstAirDate':tvShowDetails[7],
            'tvShowSeasonEpisodesNum':tvShowDetails[9],
            'tvShowVideo': video,
            'season_num': season_num,
            'show_ID': show_ID,
            'message': 'Description for the page',
            'year': datetime.now().year,
            'ep_details': zip(ep_names, ep_IDs, ep_posters),
        }
    )

def episode_details(request, show_ID, season_num, episode_num):
    assert isinstance(request, HttpRequest)

    episodeDetails, crewStuffs, guestStuffs = fetch.fetch.get_episode_details(show_ID, season_num, episode_num)
    
    if crewStuffs == []:
        crews = ""
        crewPics = ""
        crewIDs = ""
        crewCharacters = ""
        crewDepartments = ""
        crewJobs = ""
    else:    
        crews = crewStuffs[0]
        crewPics = crewStuffs[1]
        crewIDs = crewStuffs[2]
        crewDepartments = crewStuffs[3]
        crewJobs = crewStuffs[4]

    if guestStuffs == []:
        guests = ""
        guestPics = ""
        guestIDs = ""
        guestCharacters = ""

    else:    
        guests = guestStuffs[0]
        guestPics = guestStuffs[1]
        guestIDs = guestStuffs[2]
        guestCharacters = guestStuffs[3]

    return render(
        request,
        'app/episode_details.html',
        {
            'title':'TV Shows',
            'showCrews': zip(crews, crewPics, crewIDs, crewDepartments, crewJobs),
            'showGuests': zip(guests, guestPics, guestIDs, guestCharacters),
            'epAirDate': episodeDetails[0],
            'epName': episodeDetails[1],
            'epOverview': episodeDetails[2],
            'epPoster': episodeDetails[5],
            'epVote': episodeDetails[6],
            'epVoteCount':episodeDetails[7],
            'episodeNum':episode_num,
            'seasonNum':season_num,
        }
    )

def actor_details(request, cast_ID):
    assert isinstance(request, HttpRequest)
    actorBios, actorPosters, stuff = fetch.fetch.get_actor_details(cast_ID)

    if stuff == []:
        names = ""
        voteCounts = ""
        voteAverages = ""
        firstAirDates = ""
        posterPaths = ""
        backdropPaths = ""
        overviews = ""
        popularities = ""
        characters = ""
        creditIds = ""
        episodeCounts = ""

    else:    
        names = stuff[0]
        voteCounts = stuff[1]
        voteAverages = stuff[2]
        firstAirDates = stuff[3]
        posterPaths = stuff[4]
        backdropPaths = stuff[5]
        overviews = stuff[6]
        popularities = stuff[7]
        characters = stuff[8]
        creditIds = stuff[9]
        episodeCounts = stuff[10]

    return render(
        request,
        'app/actors.html',
        {
            'title':'TV Shows',
            "adult": actorBios[0],
            "biography": actorBios[1],
            "birthday": actorBios[2],
            "deathday": actorBios[3],
            "gender": actorBios[4],
            "homepage": actorBios[5],           
            "imdb_id": actorBios[6],     
            "department": actorBios[7],
            "name": actorBios[8],
            "placeOfBirth": actorBios[9],           
            "profilePath": actorBios[10],    
            "popularity": actorBios[11],    
            'actorDetails': zip(names, voteCounts, voteAverages, firstAirDates, posterPaths, backdropPaths, overviews, popularities, characters, creditIds, episodeCounts),
            'actorPhotos': actorPosters,
        }
    )

