import json

data='''{
    "name": "Radiohead",
    "popularity": 78,
    "debut_album" :  {
        "name": "Pablo Honey",
        "year": 1993
        },
    "genres": ["alternative rock",
             "indie rock",
             "melancholia",
             "permanent wave",
             "rock"]
             }'''

info=json.loads(data)


print 'Name:', info['name']
print 'Genre:', info['genres'][0]
print 'Album:', info['debut_album']['name']