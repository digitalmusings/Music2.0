from lyricsgenius import Genius
from lyricsgenius.utils import clean_str
from cobe.brain import Brain
from decouple import config
import sys
import re
import json
import os
import argparse


# Parse arguments
parser = argparse.ArgumentParser(
    prog='Jukebox',
    description='Add new songs to brain',
    epilog=''
)
parser.add_argument( 'artist', help = 'The artist to pull lyrics for' )
parser.add_argument( '--max', '-m', type = int, help = 'The max number of songs to pull' )
parser.add_argument( '--batch', '-b', 
                     type = int, 
                     default = 5, 
                     help = 'How many songs to pull at a time' 
)
args = parser.parse_args()

# Instantiate Genius and define search parameters
genius = Genius(config('GENIUS_TOKEN'))
genius.remove_section_headers = True
genius.skip_non_songs = True

exc_terms = [ 'acoustic', 'remix', 'mix$', 'live$', 'live at', 
              'live in', 'demo$', 'version', 'DVD', 'edit$',
              'booklet', 'album', 'live from', 'extended' ]

# Grab existing song titles to add to exclusion list
# pattern = re.compile( '([\[\]$&+,:;=?@#\'<>.^*()%!-])' )
if os.path.isfile( 'lyrics.json' ):
    with open( 'lyrics.json', 'r' ) as file:
        artists = json.load( file )
    titles = []
    found_artist = next( ( artist for artist in artists if artist[ "artist" ] == args.artist ), None )
    if found_artist:
        for s in found_artist[ "songs" ]:
            # titles.append( re.sub( pattern, r'\\\1', s["title"] ) )
            titles.append( clean_str( s['title'] ) )
        for s in titles:
            exc_terms.append( s )
        print( titles )
genius.excluded_terms = exc_terms

# set pull variables
batch_size = 5 if args.batch is None else args.batch
remaining = 250 if args.max is None else args.max


# Start pulling the data in batches
songs = []
while remaining > 0: 
    # Pull the data 
    try:
        batch = genius.search_artist( args.artist, max_songs = batch_size )
        remaining -= batch_size
        batch_size = min( [ remaining, batch_size ] )
    except KeyboardInterrupt:
        print( 'User cancelled. Quitting.')
        sys.exit()
    except:
        print( 'Error. Retrying batch.' )
        continue

    # Remove ads and insert missing periods at the end of each line
    for s in batch.songs:
        song_clean = {
            'title': s.title,
            'lyrics': 
                re.sub( r'(^.*Get tickets as low as.*$|^.*You might also like.*$|[0-9]*Embed$)', '',
                    re.sub( r'^.*$', '',
                        re.sub( r'((\?|,|!|\.))\.$', '\1',
                            s.lyrics.replace( '\n\n', '\n' )
                                .replace( '\n', '.\n' ),
                            0,
                            re.MULTILINE
                        ),
                        1,
                        re.MULTILINE
                    ),
                    0,
                    re.MULTILINE
                )
        }
        songs.append( song_clean )
        exc_terms.append( re.escape( s.title ) )
        genius.excluded_terms = exc_terms

# Uncomment to save full output to disk.
# artist.save_lyrics( overwrite = True )

artist_dict = { 'artist': batch.name, 'songs': songs }

# Save lyrics by artist to JSON file
if not os.path.isfile( 'lyrics.json' ):
    with open( 'lyrics.json', 'w' ) as file:
        file.write( '[]' )

with open( 'lyrics.json', 'r+' ) as file:
        artists = json.load( file )
        existing_artist = next( ( artist for artist in artists if artist[ "artist" ] == args.artist ), None )
        if existing_artist:
            for s in artist_dict[ 'songs' ]:
                existing_artist[ 'songs' ].append( s )
        else:
            artists.append( artist_dict )
        file.seek( 0 )
        json.dump( artists, file, indent = 4 )


# Done looping. Finish up.
# Get just the lyrics
output = ''
for s in songs:
    output += s.get('lyrics')
# print( output )

# Write them to a temporary file
with open( 'buffer.txt', 'a+' ) as f:
    f.write( output )
    f.seek( 0 )
    # buffer = f.read()
    # print( buffer )

# Call cobe from the command line to learn from the temp file, then delete it
os.system( 'poetry run cobe -b brain.brn learn buffer.txt' )
os.remove( 'buffer.txt' )

# Open or create the brain and reply to a test question.
brain = Brain( 'brain.brn' )
reply = brain.reply( 'What''s black?' )
print( reply )
