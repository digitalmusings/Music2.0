# This example requires the 'message_content' intent.

import discord
from random import randint
from cobe.brain import Brain
from decouple import config

BOT_TOKEN               = config('BOT_TOKEN')
TRIGGER_ENABLED         = bool(config("TRIGGER_ENABLED"))
TRIGGER_WORDS           = [x.lower() for x in config("TRIGGER_WORDS").split(",")]
CHAT_ALLOWLIST          = config("CHAT_ALLOWLIST").split(",")
RANDOM_ENABLED          = bool(config("RANDOM_ENABLED"))
RANDOM_RATIO            = config("RANDOM_RATIO")
PRIVATE_REPLY_ENABLED   = bool(config("PRIVATE_REPLY_ENABLED"))
BLOCKLIST_WORDS         = config("BLOCKLIST_WORDS").split(",")
LEARN_ENABLED           = bool(config("LEARN_ENABLED"))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

brain = Brain('murph/brain.brn')

# UTILITY FUNCTIONS
# Remove the first "trigger word" detected if string is beginning with it
def remove_trigger_words(string):
	trigger_word = start_with_trigger_words(string)
	if trigger_word:
		return string[len(trigger_word):]
	return string

# Return the "trigger word" the string is beginning with. None if not detected.
def start_with_trigger_words(string):
	for word in TRIGGER_WORDS:
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
    if LEARN_ENABLED:
    		brain.learn(remove_trigger_words(msg))
    if any(w in msg.lower() for w in TRIGGER_WORDS) or (RANDOM_ENABLED and randint(0, int(RANDOM_RATIO))==0):
    		reply = brain.reply(msg)
    		await message.channel.send(reply)

client.run(BOT_TOKEN)
