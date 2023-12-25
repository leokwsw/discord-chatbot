import discord
from src.logger import logger

intents = discord.Intents.default()
intents.message_content = True


class DiscordClient(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=intents)
        self.synced = False
        self.added = False
        self.tree = discord.app_commands.CommandTree(self)
        self.activity = discord.Activity(type=discord.ActivityType.watching, name="/chat | /reset | /imagine | /clear")

    # async def on_ready(self):
    #     await self.wait_until_ready()
    #     logger.info("Syncing")
    #     if not self.synced:
    #         await self.tree.sync()
    #         self.synced = True
    #     if not self.added:
    #         self.added = True
    #     logger.info(f"Synced, {self.user} is running!")
