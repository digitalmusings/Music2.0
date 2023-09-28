import argparse
from decouple import config
import discogs_client


# Parse arguments
parser = argparse.ArgumentParser(
    prog = 'Discogs',
    description = 'Search for a release',
    epilog = ''
)
parser.add_argument( 'search', help = 'What to search for' )
parser.add_argument( 'type', 
                     default = 'master', 
                     help = 'What type of thing to search for' 
)
args = parser.parse_args()

disc = discogs_client.Client( '#Music2.0/0.1', user_token = config( 'DISCOGS' ) )

results = disc.search( args.search, type = args.type )

print( results[0] )