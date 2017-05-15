import requests
from requests.auth import HTTPBasicAuth
from credentials import  CLIENT_ID, CLIENT_TOKEN

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
        try:
            artist_id = info['artists']['items'][0]['id']
        except IndexError:
            print 'Artist not found :('
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

        if req.status_code==200:
            info=req.json()
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


    if req.status_code==200:
        info=req.json()
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


def get_auth():
    access_token=None
    accounts_service_url='https://accounts.spotify.com/api/token'

    ##CLIENT AUTHORIZATION
    auth=requests.post(url=accounts_service_url,
                       auth=HTTPBasicAuth(CLIENT_ID, CLIENT_TOKEN),
                       data={ 'grant_type': 'client_credentials'}
                       )

    if auth.status_code==200:
        auth_json=auth.json( )
        access_token=auth_json['access_token']

    else:
        print 'AUTHENTICATION FAILED'
        print auth.text
    return access_token


def get_tracks_valence(track_ids):

    valence_dict={}
    access_token=get_auth()
    params= {'ids': ','.join(track_ids)}

    headers = {'Authorization' : 'Bearer %s' % access_token }
    req= requests.get(url=service_url+'audio-features',
                  params=params,
                  headers=headers
                  )
    print 'CALLING: ', req.url


    if req.status_code==200:
        info=req.json()
        for i in info['audio_features']:
            valence_dict.update({i['id']: i['valence']})

    else:
        print 'Retrieval failed'
        print req.text

    return valence_dict



while True :
    artist_name=raw_input('Enter artist name:')
    if len(artist_name)<1: break
    album_ids=get_artist_albums(artist_name)
    print 'Total number of albums:' , len(album_ids)
    tracks={}
    for id in album_ids:
        tracks.update(get_album_tracks(id))
    print 'Total number of tracks:' , len(tracks)
    if tracks:
        track_ids=tracks.keys()
        ## Maximum: 100 IDs in this en point.
        if len(track_ids)>100:
            track_ids=track_ids[:100]
        tracks_valence=get_tracks_valence(track_ids)

        ##let's sort the tracks in descending order of valence
        sorted_list = [(k,v) for v,k in sorted([(v,k) for k,v in tracks_valence.items()], reverse=True )]
        print 'The happiest song by %s : %s' % (artist_name, tracks[sorted_list[0][0]])
        print 'The saddest song by %s : %s' % (artist_name, tracks[sorted_list[len(track_ids)-1][0]])















