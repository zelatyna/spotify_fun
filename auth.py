import requests
from requests.auth import HTTPBasicAuth
from credentials import CLIENT_ID, CLIENT_TOKEN

accounts_service_url='https://accounts.spotify.com/api/token'

##CLIENT AUTHORIZATION
auth=requests.post(url=accounts_service_url,
                   auth=HTTPBasicAuth(CLIENT_ID, CLIENT_TOKEN),
                   data={ 'grant_type': 'client_credentials'}
                   )

if auth.status_code==200:
    auth_json=auth.json( )
    print auth_json
    access_token=auth_json['access_token']

else:
    print 'AUTHENTICATION FAILED'
    print auth.text


##GET TRACK FEATURES USING THE ACCESS TOKEN (pass it in header)

service_url='https://api.spotify.com/v1/audio-features'

params= {'ids': '3pcCifdPTc2BbqmWpEhtUd'}
headers = {'Authorization' : 'Bearer %s' % access_token }

req= requests.get(url=service_url,
                  params=params,
                  headers=headers
                  )

audio_features=req.json()
print audio_features