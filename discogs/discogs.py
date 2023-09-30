import argparse
import discogs_client
import os

# Parse arguments
parser = argparse.ArgumentParser(
    prog="Discogs", description="Search for a release", epilog=""
)
parser.add_argument("search", help="What to search for")
parser.add_argument("--type", default="master", help="What type of thing to search for", choices=["master", "release", "artist"])
args = parser.parse_args()


disc = discogs_client.Client("#Music2.0/0.1")
disc.set_consumer_key(os.environ.get("DISCOGS_KEY"), os.environ.get("DISCOGS_SECRET"))

results = disc.search(args.search, type=args.type)

result = results[0]

print(result)