from typing import Dict, List
from collections import defaultdict

from src.memoryInterface import MemoryInterface


class Memory(MemoryInterface):
    def __init__(self, system_message):
        self.storage = defaultdict(list)
        self.system_message = system_message

    def initialize(self, user_id: str):
        self.storage[user_id] = [{
            'role': 'system', 'content': self.system_message
        }]

    def append(self, user_id: str, message: Dict) -> None:
        if not self.storage[user_id]:
            self.initialize(user_id)
        self.storage[user_id].append(message)

    def get(self, user_id: str) -> List[Dict]:
        return self.storage[user_id]

    def remove(self, user_id: str) -> None:
        self.storage[user_id] = []

    def clear(self) -> None:
        self.storage.clear()
