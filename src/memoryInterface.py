from typing import Dict, List


class MemoryInterface:
    def append(self, user_id: str, message: Dict) -> None:
        pass

    def get(self, user_id: str) -> List[Dict]:
        return []

    def remove(self, user_id: str) -> None:
        pass

    def clear(self) -> None:
        pass