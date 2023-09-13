from lyricsgenius import Genius
from cobe.brain import Brain
from decouple import config

genius = Genius(config('GENIUS_TOKEN'))

genius.remove_section_headers = True
genius.skip_non_songs = True
genius.excluded_terms = ["(mix)", "(Live)", "(Demo)", "(Version)", "(DVD)", "(Edit)"]

artist = genius.search_artist('Muse')
artist.save_lyrics()

# The following command will produce the output we want, apart from the ads.
# Maybe use ChatGPT to remove them?
# jq '{ (.name): [.songs[] | select(.title | test("(?i)(live|mix|demo|version|DVD|edit)"; "i") | not) | {(.title): .lyrics}] }' Lyrics_Muse.json > muse_lyrics.json
