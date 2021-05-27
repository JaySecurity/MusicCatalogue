import json
import os

import requests

headers = {
    'x-rapidapi-key': os.getenv('X-RAPIDAPI-KEY'),
    'x-rapidapi-host': os.getenv('X-RAPIDAPI-HOST')
    }

# url = "https://theaudiodb.p.rapidapi.com/search.php"

# querystring = {"s":"Screeching Weasel"}

# response = requests.request("GET", url, headers=headers, params=querystring)
# data= response.json()

# print(data)
# artist_id = data['artists'][0]['idArtist']
# print(artist_id)


# url = "https://theaudiodb.p.rapidapi.com/album.php"

# querystring = {"i":artist_id}


# response = requests.request("GET", url, headers=headers, params=querystring)



# data = response.json()

# albums = data['album']

# for album in albums:
#   print(f"{album['strAlbum']}  --   {album['intYearReleased']}")

# url = "https://theaudiodb.p.rapidapi.com/searchalbum.php"

# querystring = {"s":"Screeching Weasel","a":"Bark like a dog"}

# response = requests.get(url, headers=headers, params=querystring)
# data = response.json()
# album_id = data['album'][0]['idAlbum']
# coverart_url = data['album'][0]['strAlbumThumb']

# url = "https://theaudiodb.p.rapidapi.com/track.php"

# querystring = {"m":album_id}
# response = requests.get(url, headers=headers, params=querystring)
# data = response.json()
# tracks = data['track']
# for track in tracks:
#   print(f"{track['intTrackNumber']} - {track['strTrack']} ")

musicbrainzid = "c8b03190-306c-4120-bb0b-6f2ebfc06ea9"
apikey = "tJVWLOEZgfxYjes0"
url = "https://api.songkick.com/api/3.0/artists/mbid:" + musicbrainzid + "/calendar.json?apikey=" + apikey
response = requests.get(url)
concert = response.json()['resultsPage']['results']['event'][0]
displayName = concert['start']['date']
print(displayName)
print(url)

