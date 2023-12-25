from src.models import ModelInterface
from src.memory import MemoryInterface


class ChatGPT:
    def __init__(self, model: ModelInterface, memory: MemoryInterface):
        self.model = model
        self.memory = memory

    async def get_response(self, user_id: int or str, text: str) -> str:
        if user_id != 0:
            self.memory.append(user_id, {'role': 'user', 'content': text})

        if user_id != 0:
            response = await self.model.chat_completion(self.memory.get(user_id))
        else:
            response = await self.model.chat_completion([{'role': 'system', 'content': text}])
        role = response[0]
        content = response[1]
        if user_id != 0:
            self.memory.append(user_id, {'role': role, 'content': content})
        return content

    def clean_history(self, user_id: int or str) -> None:
        self.memory.remove(user_id)

    def clear(self) -> None:
        self.memory.clear()
