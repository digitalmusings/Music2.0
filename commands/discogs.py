import argparse
import discogs_client
from decouple import config

# Parse arguments
parser = argparse.ArgumentParser(
    prog="Discogs", description="Search for a release", epilog=""
)
parser.add_argument("track", help="What track to search for")
parser.add_argument("artist", help="The artist the track is by")
parser.add_argument("--type", default="master", help="What type of thing to search for", choices=["master", "release", "artist"])
args = parser.parse_args()

disc = discogs_client.Client("#Music2.0/0.1", user_token=config("DISCOGS_TOKEN"))
# disc.set_consumer_key(os.environ.get("DISCOGS_KEY"), os.environ.get("DISCOGS_SECRET"))

# Search for the artist
results = disc.search(args.artist, type="artist")
artist = results[0]

results = disc.search(track=args.track, artist=artist.name, type=args.type, sort="year", sort_order="asc")

formats_to_include = ["Album", "Single", "Compilation", "LP"]
results = [release for release in results if any(format in formats_to_include for format in release.data['format'])
           and not any(format in ["Promo", "EP", "Unofficial Release", "Test Pressing"] for format in release.data['format'])]

results = sorted(results, key = lambda x: (int(x.data['year']) if 'year' in x.data else 9999,
                                           0 - x.data['community']['want'] - x.data['community']['have']))

if results:
    release_arr = []
    single_year = 9999
    for result in results:
        release = disc.master(result.data['id'])
        if any(track.title.lower() == args.track.lower() for track in release.tracklist):
            if len(release_arr) == 0:
                rls = { 'release': release, 'result': result }
                release_arr.append(rls)
                if 'Single' in result.data['format']:
                    single_year = int(release.year)
                else:
                    break
            elif 'Single' not in result.data['format']:
                if ( single_year != 9999 and 'Compilation' not in result.data['format'] 
                    ) or ( single_year == 9999 and 'Compilation' in result.data['format'] ):
                    rls = { 'release': release, 'result': result }
                    release_arr.append(rls)
                    break
            elif int(release.year) - single_year > 5:
                break
    else:
        print("No release found")
else:
    print("No results found")


for idx, rls in enumerate(release_arr):
    track = [track.title for track in rls['release'].tracklist if track.title.lower() == args.track.lower()][0]
    if idx == 0:
        print(track)
    print('------------------')
    line_1 = rls['release'].data['title'] + ' (' + str(rls['release'].data['year']) + ') ' + rls['result'].data['country']
    line_2 = rls['result'].data['format']
    print(line_1)
    print(line_2)