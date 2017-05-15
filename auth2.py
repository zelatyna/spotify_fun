import requests
from requests.auth import HTTPBasicAuth
from credentials import  CLIENT_ID, CLIENT_TOKEN, CLIENT_URI

def get_access_token():
    access_token=None
    #1. Your application requests authorization
    accounts_service_url='https://accounts.spotify.com/authorize'
    #QUERY PARAMETERs
    params={
        'client_id': CLIENT_ID,
        'response_type':'code',
        'redirect_uri':CLIENT_URI,
        'scope': 'playlist-modify-private'
    }
    auth=requests.post(url=accounts_service_url,
                       auth=HTTPBasicAuth(CLIENT_ID, CLIENT_TOKEN),
                       data={ 'grant_type': 'client_credentials'}
                       )

    oauth_url=requests.get(accounts_service_url, params).url

    ##2. The user is asked to authorize access within the scopes
    import webbrowser
    try:
        webbrowser.open(oauth_url)
        print ('Opened %s in your browser' % oauth_url)
    except:
        print ('Please navigate here %s' % oauth_url)


    ##3. The user is redirected back to your specified URI
    try:
        response = raw_input('Enter the URL you were redirected to:')
    except NameError:
        response = input('Enter the URL you were redirected to:')

    ##parse the code from url
    code=response.split('?code=')[1].split('&')[0].strip()


    ##4. Your application requests refresh and access tokens
    accounts_service_token_url = 'https://accounts.spotify.com/api/token'
    data ={
        'code': code,
        'grant_type':'authorization_code',
        'redirect_uri':CLIENT_URI,
        'scope': 'playlist-modify-private'
    }

    req_token=requests.post(url=accounts_service_token_url,
                            data=data,
                            auth=HTTPBasicAuth(CLIENT_ID, CLIENT_TOKEN),
                            verify=True)

    ##5. The tokens are returned to your application
    if req_token.status_code==200:
        token_info=req_token.json()
        access_token=token_info['access_token']
        print 'Authorization Code Flow completed successfully '
        print access_token
    else:
        print req_token.reason

    return access_token

##we will just store it and use in the final code
