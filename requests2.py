import requests

service_url='https://api.spotify.com/v1/'


def search_artist_id(artist_name):

    endpoint='search'
    params= {'q': artist_name,
            'type': 'artist'}

    req= requests.get(url=service_url+endpoint, params=params)
    print 'CALLING:', req.url

    artist_id= None
    if req.status_code==200:
        info=req.json()
        artist_id = info['artists']['items'][0]['id']
    else:
        print 'Retrieval failed'
        print req.text
    return artist_id