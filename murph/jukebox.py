from lyricsgenius import Genius
from cobe.brain import Brain
from decouple import config
import sys
import re
import json
import os

genius = Genius(config('GENIUS_TOKEN'))

genius.remove_section_headers = True
genius.skip_non_songs = True
genius.excluded_terms = ["mix\)", "\(Live", "Demo\)", "Version\)", "DVD", "Edit\)"]

arg_cnt = len(sys.argv)
search_term = sys.argv[1]

if arg_cnt == 2: 
    artist = genius.search_artist( search_term )
elif arg_cnt == 3:
    search_max = int( sys.argv[2] )
    artist = genius.search_artist( search_term, max_songs = search_max )
else: 
    sys.exit('Arguments: search_artist(s) [max_songs] [sort_by]')

# artist.save_lyrics( overwrite = True )

songs = []
for s in artist.songs:
    songs.append( 
        {   'title': s.title,
            'lyrics': 
                re.sub( r'^.*Get tickets as low as.*$', '',
                    re.sub( r'^.*$', '',
                        re.sub( r'[0-9]+Embed', '', 
                            s.lyrics.replace( '\n\n', '\n' ).replace( '\n', '.\n' ) ),
                        1,
                        re.MULTILINE
                    ),
                    0,
                    re.MULTILINE
                )
        }
    )

artist_dict = { 'artist': artist.name, 'songs': songs }

artist_json = json.dumps(artist_dict, indent=4)

f = open( 'lyrics.json', 'w' )
f.write( artist_json )
f.close()

output = ''
for s in songs:
    output += s.get('lyrics')

# print( output )
f = open( 'buffer.txt', 'w' )
f.write( output )
f.close()

os.system( 'poetry run cobe -b brain.brn learn buffer.txt' )
os.remove( 'buffer.txt' )

brain = Brain( 'brain.brn' )
reply = brain.reply( 'What''s black?' )
print( reply )
