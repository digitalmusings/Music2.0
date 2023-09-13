from lyricsgenius import Genius
from cobe.brain import Brain
from decouple import config
import sys
import re
import pprint as pp

genius = Genius(config('GENIUS_TOKEN'))

genius.remove_section_headers = True
genius.skip_non_songs = True
genius.excluded_terms = ["mix\)", "\(Live", "Demo\)", "Version\)", "DVD", "Edit\)"]

search_terms = sys.argv[1]
search_max = 0 if len(sys.argv) != 3 else int(sys.argv[2])

artist = genius.search_artist( search_terms, max_songs=search_max )

lyrics_json = { (artist.name): list(
    map( lambda s:
        {
            s.title:
            re.sub( r'^.*Get tickets as low as.*$', '',
                re.sub( r'^.*$', '',
                    re.sub( r'[0-9]+Embed', '', s.lyrics ),
                    1,
                    re.MULTILINE
                ),
                0,
                re.MULTILINE
            )
        },
        artist.songs
    )
) }

# print(lyrics_json)
pp.pprint(lyrics_json)

artist.save_lyrics()

# The following command will produce the output we want, apart from the ads.
# Maybe use ChatGPT to remove them?
# jq '{ (.name): [.songs[] | select(.title | test("(?i)(live|mix|demo|version|DVD|edit)"; "i") | not) | {(.title): .lyrics}] }' Lyrics_Muse.json > muse_lyrics.json
