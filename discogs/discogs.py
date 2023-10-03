import argparse
import discogs_client
from decouple import config
import operator

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
    for result in results:
        release = disc.master(result.data['id'])
        if any(track.title.lower() == args.track.lower() for track in release.tracklist):
            track = [track.title for track in release.tracklist if track.title.lower() == args.track.lower()][0]
            print('track', track)
            break
    if release:
        for key, value in release.data.items():
            if key in ['title', 'format', 'year', 'country']:
                print(key, value)
        print('formats', result.data['format'])
        print('country', result.data['country'])
    else:
        print("No release found")
else:
    print("No results found")