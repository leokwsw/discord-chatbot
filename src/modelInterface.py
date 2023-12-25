from typing import List, Dict


class ModelInterface:
    def chat_completion(self, messages: List[Dict]) -> (str, str):
        pass

    def image_generation(self, prompt: str) -> str:
        pass
