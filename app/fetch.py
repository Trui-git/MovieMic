
from django.http import response
import requests
import json
from datetime import datetime, timedelta

api_key = "60918711ab06f46cb045b0ee80dcebd9" # your api_key from TMDB

class fetch():
    
    def get_onTV():

        today = datetime.today()
        currentDay = str(today.year)+ '-' + str(today.month) + '-' + str(today.day)
        date_14_later =  today + timedelta(days=15)
        futurDay = str(date_14_later.year) + '-' + str(date_14_later.month) + '-' + str(date_14_later.day)

        url = "https://api.themoviedb.org/3/discover/tv?api_key=" + api_key + "&primary_release_date.gte=" + currentDay + "&primary_release_date.lte=" + futurDay
        response = requests.get(url)
        stuff = []

        if(response.ok): # 200 ok
            jData = json.loads(response.content)
            data = jData['results']
            posters = []
            ids = []
            titles =[]

            for idx in range(len(data)):
                posterPath = data[idx]['poster_path']
                posters.append(posterPath)
                showID = data[idx]['id']
                ids.append(showID)
                title = data[idx]['name']
                titles.append(title)

            stuff.append(posters)
            stuff.append(ids)
            stuff.append(titles)   
        else:
            stuff = None
        return stuff

    def get_shows(searchTerm):
        url = "https://api.themoviedb.org/3/search/tv?api_key=" + api_key  + "&language=en-US&query=" + searchTerm
        response = requests.get(url)
        stuff = []

        if(response.ok): # 200 ok
            jData = json.loads(response.content)
            data = jData['results']
            posters = []
            ids = []
            titles =[]

            for idx in range(len(data)):
                posterPath = data[idx]['poster_path']
                posters.append(posterPath)
                showID = data[idx]['id']
                ids.append(showID)
                title = data[idx]['name']
                titles.append(title)

            stuff.append(posters)
            stuff.append(ids)
            stuff.append(titles)   
        else:
            stuff = None
        return stuff

    def get_seasons(showID):
        url = "https://api.themoviedb.org/3/tv/" + showID + "?api_key=" + api_key
        response = requests.get(url)
        stuff = []

        global masterTvID
        masterTvID = showID

        if(response.ok):
            jData = json.loads(response.content)
            data = jData['seasons']

            images = []
            titles = []
            seasonNums = []
            overviews = []

            for idx in range(len(data)):
                title = data[idx]['name']
                titles.append(title)
                image = data[idx]['poster_path']
                images.append(image)
                snum = data[idx]['season_number']
                seasonNums.append(snum)
                overview = data[idx]['overview']
                overviews.append(overview)

            stuff.append(images)
            stuff.append(titles)
            stuff.append(seasonNums)
            stuff.append(overviews)
        else:
            stuff = None

        return stuff

    def get_episodes(season_num):
        global master_season_num
        master_season_num = season_num

        url = "https://api.themoviedb.org/3/tv/" + masterTvID + "/season/" + season_num + "?api_key=" + api_key
        response = requests.get(url)
        stuff = []

        if(response.ok):
            jData = json.loads(response.content)
            data = jData['episodes']
            titles = []
            epNums = []
            posters = []

            for idx in range(len(data)):
                title = data[idx]['name']
                titles.append(title)
                epNum = data[idx]['episode_number']
                epNums.append(epNum)
                poster = data[idx]['still_path']
                posters.append(poster)

            stuff.append(titles)
            stuff.append(epNums)
            stuff.append(posters)
        else:
            stuff = None
        
        return stuff

    def get_season_details():
        seasonUrl = "https://api.themoviedb.org/3/tv/" + masterTvID + "?api_key=" + api_key
        
        response = requests.get(seasonUrl)
        creatorStuff = []
        tvShowDetails = []
        
        tvShowPoster =""
        tvShowDetailsRequests = ["id", "original_name", "overview", "vote_average", "number_of_seasons", "number_of_episodes"]
        if(response.ok):
            jData = json.loads(response.content)
            tvShowPoster =jData['poster_path']
            creatorsData = jData['created_by']
            
            creatorNames = []
            creatorPosters =[]            

            for idx in range(len(creatorsData)):
                cName = creatorsData[idx]['name']
                creatorNames.append(cName)
                cProfilePic = creatorsData[idx]['profile_path']
                creatorPosters.append(cProfilePic)
                
            for items in tvShowDetailsRequests:
                value = jData[items]
                tvShowDetails.append(value)

            creatorStuff.append(creatorNames)
            creatorStuff.append(creatorPosters)
        else:
            creatorStuff = None

        creditsUrl = "https://api.themoviedb.org/3/tv/" + masterTvID + "/credits?api_key=" + api_key
        
        response = requests.get(creditsUrl)
        creditDetails = []
        if(response.ok):
            jData = json.loads(response.content)
            castDetails =jData['cast']

            castNames = []
            castPosters =[]
            castIDs = []
            for idx in range(len(castDetails)):
                name = castDetails[idx]['name']
                castNames.append(name)
                profilePic = castDetails[idx]['profile_path']
                castPosters.append(profilePic)
                ids = castDetails[idx]['id']
                castIDs.append(ids)
                creditDetails.append(castNames)
                creditDetails.append(castPosters)
                creditDetails.append(castIDs)
        else:
            creditDetails = None
        
        imagesUrl = "https://api.themoviedb.org/3/tv/" + masterTvID + "/images?api_key=" + api_key
        
        response = requests.get(imagesUrl)
        imagesDetails = []
        if(response.ok):
            jData = json.loads(response.content)
            backdropDetails =jData['backdrops']
            imagePaths =[]
            
            for idx in range(len(backdropDetails)):
                image = backdropDetails[idx]['file_path']
                imagesDetails.append(image)   
        else:
            imagesDetails = None

        return creatorStuff,tvShowDetails,tvShowPoster,creditDetails,imagesDetails

    def get_videoFromId(id):
        url = "https://api.themoviedb.org/3/tv/" + str(id)  + "/videos?api_key=" + api_key + "&language=en-US"
        response = requests.get(url)
        keys = []

        if(response.ok): # 200 ok
            jData = json.loads(response.content)
            data = jData['results']


            for idx in range(len(data)):
                key = data[idx]['key']
                keys.append(key)
 
        else:
            keys = None
        return keys

    def get_search_result_details(tvShowIDs):
        stuff = []
        overviews = []
        homepages = []
        backdrops = []

        for idx in tvShowIDs:
            url = "https://api.themoviedb.org/3/tv/" + str(idx) + "?api_key=" + api_key
            response = requests.get(url)
            if(response.ok):
                jData = json.loads(response.content)
                overview_data = jData['overview']
                homepage_data = jData['homepage']
                backdrop_path_data = jData['backdrop_path']
                overviews.append(overview_data)
                homepages.append(homepage_data)
                backdrops.append(backdrop_path_data)

        stuff.append(overviews)
        stuff.append(homepages)
        stuff.append(backdrops)

        return stuff