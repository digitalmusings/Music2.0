from tzstamp import tzstamp
from disc import disc
from tight import tight
from xkcd import xkcd


class SlashCommander:
    @staticmethod
    def CONFIG():
        return {
            "tzstamp": {
                "handler": "tzstamp",
                "global": True,
                "channels": False,
                "name": "tzstamp",
                "description": "Replaces a message's datetimes in yyyy/MM/dd HH:mm format with Discord dynamic time zone format.",
                "options": [
                    {
                        "name": "msg",
                        "type": "STRING",
                        "description": "The message containing the datetime.",
                        "required": True,
                    },
                    {
                        "name": "offset",
                        "type": "STRING",
                        "description": 'The offset from UTC in the format "UTC[+/-]X". Defaults to UTC.',
                        "required": False,
                        "defaultValue": "UTC+0",
                    },
                    {
                        "name": "raw",
                        "type": "BOOLEAN",
                        "description": "Return the timestamp code in a codeblock.",
                        "required": False,
                        "defaultValue": False,
                    },
                ],
            },
            "disc": {
                "handler": "disc",
                "global": True,
                "channels": ["music", "music-meta", "skynet"],
                "name": "disc",
                "description": "Returns the earliest year of the specified track according to Discogs.",
                "options": [
                    {
                        "name": "artist",
                        "type": "STRING",
                        "description": "The artist to search for.",
                        "required": True,
                    },
                    {
                        "name": "title",
                        "type": "STRING",
                        "description": "The track to search for.",
                        "required": True,
                    },
                ],
            },
            "tight": {
                "handler": "tight",
                "global": True,
                "channels": ["music", "music-meta", "skynet"],
                "name": "tight",
                "description": "Returns a list of matches that are closer than the number of outstanding votes.",
                "options": [
                    {
                        "name": "tightest",
                        "type": "BOOLEAN",
                        "description": "Return only matches within one vote.",
                        "required": False,
                    },
                ],
            },
            "xkcd": {
                "handler": "xkcd",
                "global": False,
                "channels": ["skynet"],
                "name": "xkcd",
                "description": "Returns a the best match xkcd comic for the specified number of lines of conversation, or returns the specific comic.",
                "options": [
                    {
                        "name": "num",
                        "type": "INTEGER",
                        "description": "The number of lines of conversation to parse or the comic to fetch.",
                        "required": True,
                    },
                    {
                        "name": "get",
                        "type": "BOOLEAN",
                        "description": "Return the specified comic.",
                        "required": False,
                    },
                ],
            },
        }

    class SlashCommander:
        @staticmethod
        def get_command_data(config):
            # We overload this config setup, so make a deep copy and drop some stuff
            data = json.loads(json.dumps(config))
            del data["handler"]
            del data["global"]
            del data["channels"]
            for option in data["options"]:
                del option["defaultValue"]
            return data

    @staticmethod
    def getOption(options, name, type, defaultValue):
        val = None
        if type == "STRING":
            val = options.getString(name)
        elif type == "BOOLEAN":
            val = options.getBoolean(name)
        elif type == "INTEGER":
            val = options.getInteger(name)
        else:
            raise ValueError(f"Unrecognized option type {type}")
        if val is None:
            val = defaultValue
        return val


    @staticmethod
    def getArgs(configOptions, interaction):
        return [SlashCommander.getOption(
            interaction.options,
            configOption["name"],
            configOption["type"],
            configOption.get("defaultValue")
        ) for configOption in configOptions]


    @staticmethod
    def isValidChannel(command, interaction):
        logger.debug({'command': command, 'interaction': interaction}, 'Testing for valid channel')
        config = SlashCommander.CONFIG()[command]
        if config is None:
            raise ValueError(f"Unknown command '{command}'")
        if config['global'] and not interaction.guild_id:
            # Interaction from a DM
            # Always allowed for global commands
            return True
        if not config['channels']:
            # All channels allowed
            return True
        if not interaction.guild_id or not interaction.channel:
            # Now it needs to have a channel
            return False
        return any(channel_name == interaction.channel.name for channel_name in config['channels'])


    def __init__(self, logger, client):
        self.logger = logger.child({'class': 'SlashCommander'})
        self.client = client
        self.initialized = False

    async def init(self):
            self.logger.info('Initializing SlashCommander')
            await self.client.ready()
            self.initialized = True

    def destroy(self):
        self.client.destroy()

    class SlashCommander:
        def require_init(self):
            if not self.initialized:
                raise ValueError('SlashCommander was not initialized')

    async def start(self, commands = []):
        @self.client.client.event
        async def on_interaction_create(interaction):
            if not interaction.is_command():
                self.logger.debug('Interaction is not a command')
                return
            if (commands and interaction.command_name not in commands) or interaction.command_name not in SlashCommander.CONFIG:
                self.logger.debug(f"Not handling command '{interaction.command_name}'")
                return
            if not self.isValidChannel(interaction.command_name, interaction):
                self.logger.debug(f"Not handling command '{interaction.command_name}' in channel {interaction.channel.id if interaction.channel else None}")
                return
            self.dispatch(
                interaction.command_name,
                [SlashCommander.getOption(
                    interaction.options,
                    config_option["name"],
                    config_option["type"],
                    config_option.get("defaultValue")
                ) for config_option in SlashCommander.CONFIG[interaction.command_name]["options"]],
                interaction,
            )

    async def dispatch(self, command, args, interaction=False):
        self.logger.debug({'command': command, 'args': args}, 'Dispatching slash command')
        if command not in SlashCommander.CONFIG:
            raise ValueError(f'Unrecognized slash command {command}')
        getattr(self, SlashCommander.CONFIG[command]['handler'])(interaction, args)

    async def tzstamp(self, interaction, args):
        if interaction:
            self.logger.debug({'args': args}, 'Handling tzstamp command.')
            response = ''
            try:
                response = tzstamp(*args)
            except Exception as e:
                response = f'ERROR {e}'
            if response == args[0]:
                response = 'Could not find a suitable timestamp. Use `yyyy/MM/dd HH:mm`.'
            self.logger.debug({'args': args, 'response': response}, 'Replying to tzstamp command.')
            await interaction.reply(response)
        else:
            self.logger.info({'args': args}, 'Testing tzstamp.')
            if not args:
                self.logger.debug('No arguments given, using default')
                args = ['2022/01/03 16:50']
            self.logger.info(tzstamp(*args))


    async def disc(self, interaction, args):
        if interaction:
            self.logger.debug({'args': args}, 'Handling disc command.')
            response = ''
            try:
                response = await disc(*args)
            except Exception as e:
                response = e.message
            self.logger.debug({'args': args, 'response': response}, 'Replying to disc command.')
            await interaction.reply({'embeds': [response]})
        else:
            self.logger.info({'args': args}, 'Testing disc.')
            if len(args) == 2:
                try:
                    self.logger.info(await disc(*args))
                except Exception as e:
                    self.logger.info(e.message)
            else:
                self.logger.error('Incorrect number of arguments given. Artist and title are required.')


    async def tight(self, interaction, args):
        if interaction:
            self.logger.debug({'args': args}, 'Handling tight command.')
            response = ''
            try:
                response = await tight(self.client, *args)
            except Exception as e:
                response = e.message
            self.logger.debug({'args': args, 'response': response}, 'Replying to tight command.')
            await interaction.reply(response)
        else:
            self.logger.info({'args': args}, 'Testing tight.')

    async def xkcd(self, interaction, args):
        if interaction:
            self.logger.debug({'args': args}, 'Handling xkcd command.')
            response = ''
            try:
                response = await xkcd(self.client, interaction.channel, *args)
            except Exception as e:
                response = e.message
            self.logger.debug({'args': args, 'response': response}, 'Replying to xkcd command.')
            await interaction.reply(response)
        else:
            self.logger.info({'args': args}, 'Testing xkcd.')
            response = await xkcd(self.client, interaction.channel, *args)
            self.logger.info({'args': args}, response)


    def create_commands(commands = []):
        if not commands:
            commands = list(SlashCommander.CONFIG.keys())
        logger.info({'commands': commands}, 'Creating slash commands')
        for command in commands:
            config = SlashCommander.CONFIG[command]
            manager = None
            if config['global']:
                manager = client.client.application.commands
            else:
                manager = client.guild.commands
            asyncio.run_coroutine_threadsafe(manager.create(SlashCommander.get_command_data(config)), client.loop)

    async def get_command_id(self, command_name):
        config = SlashCommander.CONFIG[command_name]
        commands = None
        if config['global']:
            commands = self.client.client.application.commands
        else:
            commands = self.client.guild.commands
        return next((command.id for command in commands.values() if command.name == command_name), None)

    async def get_command_ids(self):
        command_ids = []
        for command_name in SlashCommander.CONFIG.keys():
            command = await self.client.client.application.commands.find(lambda c: c.name == command_name)
            command_ids.append(command.id)
        return command_ids
