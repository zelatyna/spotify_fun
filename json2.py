import json


data = file('artist.json').read()
info=json.loads(data)

##print artist name and number of followers

for artist in info['artists']['items']:
    print 'Name: ' , artist['name']
    print 'ID: ', artist['id']
    print 'Followers: ', artist['followers']['total'], '\n'








