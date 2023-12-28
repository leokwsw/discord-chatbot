import os

from dotenv import load_dotenv
import discord

from src.dalle import DALLE
from src.discordClient import DiscordClient
from src.sender import Sender
from src.logger import logger
from src.chatgpt import ChatGPT
from src.models import OpenAIModel
from src.memory import Memory

load_dotenv()

models = OpenAIModel(
    api_key=os.getenv('OPENAI_API_KEY'),
    model_engine=os.getenv('OPENAI_MODEL_ENGINE'),
    image_model_engine=os.getenv("OPENAI_IMAGE_MODEL_ENGINE")
)

config_dir = os.path.abspath(f"{__file__}/../")
prompt_name = 'system_prompt.txt'
prompt_path = os.path.join(config_dir, prompt_name)
with open(prompt_path, "r", encoding="utf-8") as f:
    starting_prompt = f.read()
    memory = Memory(system_message=starting_prompt)
chatgpt = ChatGPT(models, memory)
dalle = DALLE(models)


def run():
    client = DiscordClient()
    sender = Sender()

    @client.event
    async def on_ready():
        await client.wait_until_ready()
        logger.info("Syncing")
        if not client.synced:
            await client.tree.sync()
            client.synced = True
        if not client.added:
            client.added = True
        logger.info(f"Synced, {client.user} is running!")
        # receive = await chatgpt.get_response(0, '')
        # channel = client.get_channel(int(os.getenv('DISCORD_CHANNEL_ID')))
        # await sender.send_message_to_channel(channel=channel, receive=receive)

    @client.tree.command(name="chat", description="Have a chat with ChatGPT")
    async def chat(interaction: discord.Interaction, *, message: str):
        user_id = interaction.user.id
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        async with interaction.channel.typing():
            receive = await chatgpt.get_response(user_id, message)
            await sender.send_message(interaction, user_id=user_id, user_message=message, receive=receive,
                                      followup=True)

    @client.tree.command(name="imagine", description="Generate image from text")
    async def imagine(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return
        await interaction.response.defer()
        async with interaction.channel.typing():
            image_url = dalle.generate(prompt)
            await sender.send_image(interaction, prompt, image_url)

    @client.tree.command(name="reset", description="Reset conversation history")
    async def reset(interaction: discord.Interaction):
        user_id = interaction.user.id
        logger.info(f"resetting memory from {user_id}")
        try:
            chatgpt.clean_history(user_id)
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send(f'> Reset ChatGPT conversation history < - <@{user_id}>')
        except Exception as e:
            logger.error(f"Error resetting memory: {e}")
            await interaction.followup.send('> Oops! Something went wrong. <')

    @client.tree.command(name="remove", description="remove conversation history")
    async def remove(interaction: discord.Interaction):
        user_id = interaction.user.id
        logger.info(f"removing memory from {user_id}")
        discord_admin = os.getenv("DISCORD_ADMIN").split(",")
        if user_id in discord_admin:
            try:
                chatgpt.clear()
                await interaction.response.defer(ephemeral=True)
                await interaction.followup.send(f'> remove ChatGPT conversation history < - <@{user_id}>')
            except Exception as e:
                logger.error(f"Error resetting memory: {e}")
                await interaction.followup.send('> Oops! Something went wrong. <')
        else:
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send('> Oops! You are not admin <')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        user_id = str(message.author.id)
        username = str(message.author.name)
        user_message = str(message.content)

        if message.channel.id == int(os.getenv('DISCORD_CHANNEL_ID')):
            async with message.channel.typing():
                receive = await chatgpt.get_response(user_id, user_message)
                await sender.send_message(message, user_id=user_id, user_message=user_message, receive=receive,
                                          followup=False)

            logger.info(f"\x1b[31m{username}\x1b[0m : '{user_message}' ({message.channel})")

        client.run(os.getenv('DISCORD_BOT_TOKEN'))


if __name__ == '__main__':
    run()
