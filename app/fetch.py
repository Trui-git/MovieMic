import requests
import json

api_key = "eda2c7d3f3cec9d78106def269a4a6a4" # your api_key from TMDB

class fetch():
    
    def fetch_all_tvshows(queryTerm):
        url = "https://api.themoviedb.org/3/search/tv?api_key=" + api_key  + "&language=en-US&query=" + queryTerm
        response = requests.get(url)
        stuff = []

        if(response.ok):
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