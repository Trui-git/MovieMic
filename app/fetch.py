
from django.http import response
import requests
import json
from datetime import datetime, timedelta
import random

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

    def get_season_backdrop(show_ID, season_num):
        url = "https://api.themoviedb.org/3/tv/" + show_ID + "/season/" + str(season_num) + "?api_key=" + api_key
        response = requests.get(url)
        images = []

        if(response.ok):
            jData = json.loads(response.content)
            data = jData['episodes']
            

            for idx in range(len(data)):
                image = data[idx]['still_path']
                images.append(image)

        else:
            images = None

        if len(images) > 0:
            return images[0]
        else:
            return None


    def get_episodes(show_ID, season_num):
        global master_season_num
        master_season_num = season_num

        url = "https://api.themoviedb.org/3/tv/" + show_ID + "/season/" + season_num + "?api_key=" + api_key
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

    def get_season_details(show_ID, season_num):
        seasonUrl = "https://api.themoviedb.org/3/tv/" + show_ID + "?api_key=" + api_key
        response = requests.get(seasonUrl)
        creatorStuff = []
        tvShowDetails = []
        tvShowPoster =""
        tvShowDetailsRequests = ["id", "original_name", "overview", "vote_average", "number_of_seasons", "number_of_episodes", "episode_run_time" , "first_air_date"]
        if(response.ok):
            jData = json.loads(response.content)
            #tvShowPoster =jData['poster_path']
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

        seasonUrl = "https://api.themoviedb.org/3/tv/" + show_ID + "/season/" + str(season_num) + "?api_key=" + api_key
        response = requests.get(seasonUrl)
        episodes = []
        overview = []
        if(response.ok):
            jData = json.loads(response.content)
            tvShowPoster =jData['poster_path']
            seasonOverview = jData['overview']
            episodes = jData['episodes']
        else:
            episodes = None
            overview = None
        tvShowDetails.append(seasonOverview)
        tvShowDetails.append(len(episodes))

        creditsUrl = "https://api.themoviedb.org/3/tv/" + show_ID + "/season/" + str(season_num) + "/credits?api_key=" + api_key
        response = requests.get(creditsUrl)
        creditDetails = []
        if(response.ok):
            jData = json.loads(response.content)
            castDetails =jData['cast']
            castNames = []
            castPosters = []
            castIDs = []
            castCharacters = []
            for idx in range(len(castDetails)):
                name = castDetails[idx]['name']
                castNames.append(name)
                profilePic = castDetails[idx]['profile_path']
                castPosters.append(profilePic)
                ids = castDetails[idx]['id']
                castIDs.append(ids)
                castCharacter = castDetails[idx]['character']                
                castCharacters.append(castCharacter)
            creditDetails.append(castNames)
            creditDetails.append(castPosters)
            creditDetails.append(castIDs)
            creditDetails.append(castCharacters)
        else:
            creditDetails = None
        
        imagesUrl = "https://api.themoviedb.org/3/tv/" + show_ID + "/images?api_key=" + api_key
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

        videoUrl = "https://api.themoviedb.org/3/tv/" + show_ID  + "/videos?api_key=" + api_key + "&language=en-US"
        response = requests.get(videoUrl)
        videoKeys = []
        anyKey = 0
        returnKey = ''

        if(response.ok): # 200 ok
            jData = json.loads(response.content)
            data = jData['results']
            for idx in range(len(data)):
                videoKey = data[idx]['key']
                videoKeys.append(videoKey)

            # Generate one rumdon video
            if len(data) > 0:
                anyKey = random.randint(0,len(videoKeys)-1)
            else:
                videoKeys = None
        else:
            videoKeys = None

        if  videoKeys == None:
            returnKey = None
        else:
            returnKey = videoKeys[anyKey]

        return creatorStuff,tvShowDetails,tvShowPoster,creditDetails,imagesDetails, returnKey

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

    def get_max_seasons(show_ID):
        url = "https://api.themoviedb.org/3/tv/" + show_ID + "?api_key=" + api_key
        response = requests.get(url)
        stuff = []

        if(response.ok):
            jData = json.loads(response.content)
            stuff = jData['number_of_seasons']
        else:
            stuff = None

        return stuff

    def get_episode_details(show_ID, season_num, episode_num):
        url = "https://api.themoviedb.org/3/tv/" + show_ID + "/season/" + season_num + "/episode/" + episode_num + "?api_key=" + api_key
        response = requests.get(url)
        crewStuffs = []
        guestStuffs = []
        episodeDetails = []
        guestDetails = []
        crewDetails = []
        episodeDetailsRequests = ["air_date", "name", "overview", "id", "production_code", "still_path", "vote_average", "vote_count"]

        if(response.ok):
            jData = json.loads(response.content)
            for items in episodeDetailsRequests:
                value = jData[items]
                episodeDetails.append(value)

            crewNames = []
            crewPosters = []
            crewIDs = []
            crewDepartments = []
            crewJobs = []
            crewDetails =jData['crew']
            for idx in range(len(crewDetails)):
                name = crewDetails[idx]['name']
                crewNames.append(name)
                profilePic = crewDetails[idx]['profile_path']
                crewPosters.append(profilePic)
                ids = crewDetails[idx]['id']
                crewIDs.append(ids)
                crewDepartment = crewDetails[idx]['department']                
                crewDepartments.append(crewDepartment)
                crewJob = crewDetails[idx]['job']                
                crewJobs.append(crewJob)

            
            #find the duplicte in crewPosters
            dupltcate = {}
            for (ind,elem) in enumerate(crewNames):
                if elem in dupltcate:
                    dupltcate[elem].append(ind)
                else:
                    dupltcate.update({elem:[ind]})

            #remove the duplicated item in all info array
            for key,value in dupltcate.items():
                if len(value) > 1:
                    for i in range(1, len(value)): 
                        crewNames[value[i]] = "None"
                        crewPosters[value[i]] = "None"
                        crewIDs[value[i]] = "None"
                        crewDepartments[value[i]] = "None"
                        crewJobs[value[i]] = "None"
            
            crewNames[:] = [item for item in crewNames if item != 'None']
            crewPosters[:] = [item for item in crewPosters if item != 'None']
            crewIDs[:] = [item for item in crewIDs if item != 'None']
            crewDepartments[:] = [item for item in crewDepartments if item != 'None']
            crewJobs[:] = [item for item in crewJobs if item != 'None']
            

            crewStuffs.append(crewNames)
            crewStuffs.append(crewPosters)
            crewStuffs.append(crewIDs)
            crewStuffs.append(crewDepartments)
            crewStuffs.append(crewJobs)


            guestNames = []
            guestPosters = []
            guestIDs = []
            guestCharacters = []
            guestDetails =jData['guest_stars']
            for idx in range(len(guestDetails)):
                name = guestDetails[idx]['name']
                guestNames.append(name)
                profilePic = guestDetails[idx]['profile_path']
                guestPosters.append(profilePic)
                ids = guestDetails[idx]['id']
                guestIDs.append(ids)
                guestCharacter = guestDetails[idx]['character']                
                guestCharacters.append(guestCharacter)

            guestStuffs.append(guestNames)
            guestStuffs.append(guestPosters)
            guestStuffs.append(guestIDs)
            guestStuffs.append(guestCharacters)

        else:
            crewStuffs = None
            episodeDetails = None
            guestStuffs = None

        return episodeDetails, crewStuffs, guestStuffs

    def get_actor_details(id):
        url = "https://api.themoviedb.org/3/person/" + id + "?api_key=" + api_key
        response = requests.get(url)

        actorBios = []
        actorItems = [
            "adult", "biography", "birthday", 
            "deathday", "gender", "homepage", 
            "imdb_id", "known_for_department",
            "name", "place_of_birth", "profile_path", "popularity"]

        if(response.ok):
            jData = json.loads(response.content)
            for items in actorItems:
                value = jData[items]
                actorBios.append(value)
        else:
            actorBios = None

        url = "https://api.themoviedb.org/3/person/" + id + "/images?api_key=" + api_key
        response = requests.get(url)
        actorPosters = []
        if(response.ok):
            jData = json.loads(response.content)
            profiles =jData['profiles']
            for idx in range(len(profiles)):
                actorPoster = profiles[idx]['file_path']
                actorPosters.append(actorPoster)
        else:
            actorPosters = None

        url = "https://api.themoviedb.org/3/person/" + id + "/tv_credits?api_key=" + api_key
        response = requests.get(url)

        stuff = []
        names = []
        voteCounts = []
        voteAverages = []
        firstAirDates = []
        posterPaths = []
        backdropPaths = []
        overviews = []
        popularities = []
        characters = []
        creditIds = []
        episodeCounts = []

        if(response.ok):
            jData = json.loads(response.content)
            data =jData['cast']
            for idx in range(len(data)):
                name = data[idx]['name']
                names.append(name)

                voteCount = data[idx]['vote_count']
                voteCounts.append(voteCount)
            
                voteAverage = data[idx]['vote_average']
                voteAverages.append(voteAverage)

                if 'first_air_date' in data[idx]:
                    firstAirDate = data[idx]['first_air_date']
                    firstAirDates.append(firstAirDate)
                else:
                     firstAirDates.append("0000-00-00")

                posterPath = data[idx]['poster_path']
                posterPaths.append(posterPath)

                backdropPath = data[idx]['backdrop_path']
                backdropPaths.append(backdropPath)

                overview = data[idx]['overview']
                overviews.append(overview)
                
                popularity = data[idx]['popularity']
                popularities.append(popularity)

                character = data[idx]['character']
                characters.append(character)

                creditId = data[idx]['credit_id']
                creditIds.append(creditId)

                episodeCount = data[idx]['episode_count']
                episodeCounts.append(episodeCount)

            #find the duplicte in posterPath
            dupltcate = {}
            for (ind,elem) in enumerate(posterPaths):
                if elem in dupltcate:
                    dupltcate[elem].append(ind)
                else:
                    dupltcate.update({elem:[ind]})

            #remove the duplicated item in all info array
            for key,value in dupltcate.items():
                if len(value) > 1:
                    for i in range(1, len(value)): 
                        names[value[i]] = "None"
                        voteCounts[value[i]] = "None"
                        voteAverages[value[i]] = "None"
                        firstAirDates[value[i]] = "None"
                        posterPaths[value[i]] = "None"
                        backdropPaths[value[i]] = "None"
                        overviews[value[i]] = "None"
                        popularities[value[i]] = "None"
                        characters[value[i]] = "None"
                        creditIds[value[i]] = "None"
                        episodeCounts[value[i]] = "None"

            names[:] = [item for item in names if item != 'None']
            voteCounts[:] = [item for item in voteCounts if item != 'None']
            voteAverages[:] = [item for item in voteAverages if item != 'None']
            firstAirDates[:] = [item for item in firstAirDates if item != 'None']
            posterPaths[:] = [item for item in posterPaths if item != 'None']
            backdropPaths[:] = [item for item in backdropPaths if item != 'None']
            overviews[:] = [item for item in overviews if item != 'None']
            popularities[:] = [item for item in popularities if item != 'None']
            characters[:] = [item for item in characters if item != 'None']
            creditIds[:] = [item for item in creditIds if item != 'None']
            episodeCounts[:] = [item for item in episodeCounts if item != 'None']   

            stuff.append(names)
            stuff.append(voteCounts)
            stuff.append(voteAverages)
            stuff.append(firstAirDates)
            stuff.append(posterPaths)
            stuff.append(backdropPaths)
            stuff.append(overviews)
            stuff.append(popularities)
            stuff.append(characters)
            stuff.append(creditIds)
            stuff.append(episodeCounts)
     
        else:
            stuff = None

        return actorBios, actorPosters, stuff