from src.logger import logger


class Sender:

    def __init__(self) -> None:
        pass

    async def send_message_to_channel(self, channel, receive):
        await channel.send(receive)

    async def send_message(self, message, user_id, user_message, receive, followup=True):
        response = f'> **{user_message}** - <@{str(user_id)}> \n {receive}'
        if followup:
            await message.followup.send(response)
        else:
            await message.channel.send(response)
        logger.info(f"{user_id} sent: {user_message}, response: {receive}")

    async def send_image(self, message, send, receive):
        try:
            user_id = message.user.id
            response = f'> **{send}** - <@{str(user_id)}> \n'
            await message.followup.send(response)
            await message.followup.send(receive)
            logger.info(f"{user_id} sent: {send}, response: {receive}")
        except Exception as e:
            await message.followup.send('> **Error: Something went wrong, please try again later!**')
            logger.exception(f"Error while sending:{send} in dalle model, error: {e}")
