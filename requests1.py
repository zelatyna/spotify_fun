import requests

service_url='https://api.spotify.com/v1/search'

params= {'q': 'radiohead',
         'type': 'artist'}

req= requests.get(url=service_url, params=params)

info=req.json()

if req.status_code==200:
    for artist in info['artists']['items']:
        print 'Name: ' , artist['name']
        print 'ID: ', artist['id']
        print 'Followers: ', artist['followers']['total'], '\n'

else:
    print 'Failure'
    print req.text()





