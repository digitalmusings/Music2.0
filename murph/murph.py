# This example requires the 'message_content' intent.

import discord
from random import randint
from cobe.brain import Brain
from decouple import config

settings["BOT_TOKEN"]             = config('BOT_TOKEN')
settings["TRIGGER_ENABLED"]       = bool(config("TRIGGER_ENABLED"))
settings["TRIGGER_WORDS"]         = [x.lower() for x in config("TRIGGER_WORDS").split(",")]
settings["CHAT_ALLOWLIST"]        = config("CHAT_ALLOWLIST").split(",")
settings["RANDOM_ENABLED"]        = bool(config("RANDOM_ENABLED"))
settings["RANDOM_RATIO"]          = config("RANDOM_RATIO")
settings["PRIVATE_REPLY_ENABLED"] = bool(config("PRIVATE_REPLY_ENABLED"))
settings["BLOCKLIST_WORDS"]       = config("BLOCKLIST_WORDS").split(",")
settings["LEARN_ENABLED"]         = bool(config("LEARN_ENABLED"))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

murph = Brain('murph.brain')

# UTILITY FUNCTIONS
# Remove the first "trigger word" detected if string is beginning with it
def remove_trigger_words(string):
	trigger_word = start_with_trigger_words(string)
	if trigger_word:
		return string[len(trigger_word):]
	return string

# Return the "trigger word" the string is beginning with. None if not detected.
def start_with_trigger_words(string):
	for word in settings["TRIGGER_WORDS"]:
		if string[:len(word)].lower() == word.lower():
			return string[:len(word)]
	return None

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    if settings["LEARN_ENABLED"]:
    		bender.learn(remove_trigger_words(msg))
    if any(w in msg.lower() for w in settings["TRIGGER_WORDS"]) or (settings["RANDOM_ENABLED"] and randint(0, int(settings["RANDOM_RATIO"]))==0):
    		reply = bender.reply(msg)
    		await message.channel.send(reply)

client.run(settings["BOT_TOKEN"])
