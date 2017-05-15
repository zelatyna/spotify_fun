import requests

service_url='https://api.spotify.com/v1/'


def search_artist_id(artist_name):

    endpoint='search'
    params= {'q': artist_name,
            'type': 'artist'}

    req= requests.get(url=service_url+endpoint, params=params)
    print 'CALLING:', req.url
    info=req.json()
    artist_id= None
    if req.status_code==200:
        artist_id = info['artists']['items'][0]['id']
    else:
        print 'Retrieval failed'
        print req.text
    return artist_id


def get_artist_albums(artist_name, offset=0):
    album_ids= []
    artist_id=search_artist_id(artist_name)

    params={'album_type': 'album',
            'offset': offset}

    if artist_id:
        endpoint='artists/'+ artist_id+'/albums'
        req= requests.get(url=service_url+endpoint, params=params)
        print 'CALLING:', req.url
        info=req.json()

        if req.status_code==200:
            for i in info['items']:
                album_ids.append(i['id'])

            if info['offset'] + info['limit'] < info['total']:
                offset = offset + info['limit']
                album_ids += get_artist_albums(artist_name, offset)
        else:
            print 'Retrieval failed'
            print req.text

    return album_ids

def get_album_tracks(album_id, offset=0):
    track_ids= {}

    params={'offset': offset}

    endpoint='albums/' + id + '/tracks'
    req= requests.get(url=service_url+endpoint, params=params)
    print 'CALLING:', req.url
    info=req.json()

    if req.status_code==200:
        for i in info['items']:
            ##make sure we don't duplicate songs
            if i['id'] not in track_ids:
                track_ids.update ( { i['id'] : i['name'] } )

        if info['offset'] + info['limit'] < info['total']:
            offset = offset + info['limit']
            track_ids.update(get_album_tracks(album_id, offset))
    else:
        print 'Retrieval failed'
        print req.text
    return track_ids


while True :
    artist_name=raw_input('Enter artist name:')
    if len(artist_name)<1: break
    album_ids=get_artist_albums(artist_name)
    print 'Total number of albums:' , len(album_ids)
    track_ids=[]
    for id in album_ids:
        track_ids+=get_album_tracks(id)
    print 'Total number of tracks:' , len(track_ids)














