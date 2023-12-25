import json
from typing import List, Dict, Literal
import openai
from openai.types.chat import ChatCompletionMessage

from src.modelInterface import ModelInterface
from src.tools.google_search import search_google
from src.tools.open_weather import get_weather


class OpenAIModel(ModelInterface):
    def __init__(
            self,
            api_key: str,
            model_engine: str,
            image_size: Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"] = '512x512'
    ):
        openai.api_key = api_key
        self.model_engine = model_engine
        self.image_size = image_size

    async def chat_completion(self, messages: List[Dict] or ChatCompletionMessage) -> (str, str):
        response = openai.chat.completions.create(
            model=self.model_engine,
            messages=messages,
            tool_choice="auto",
            tools=[{
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                },
            }, {
                "type": "function",
                "function": {
                    "name": "search_google",
                    "description": "Search Google",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keyword": {
                                "type": "string",
                                "description": "Search on Google"
                            }
                        }
                    },
                    "required": ["keyword"],
                }
            }]
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            available_functions = {
                "get_current_weather": self.get_current_weather,
                "search_google": self.search_google
            }
            messages.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                if function_name == "get_current_weather":
                    function_response = await function_to_call(
                        location=function_args.get("location")
                    )
                elif function_name == "search_google":
                    function_response = await function_to_call(
                        keyword=function_args.get("keyword")
                    )
                else:
                    function_response = "Unknown tool call"

                if function_response != {}:
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        }
                    )
            second_response = openai.chat.completions.create(
                model=self.model_engine,
                messages=messages,
            )
            second_response_message = second_response.choices[0].message
            return second_response_message.role, second_response_message.content

        return response_message.role, response_message.content

    async def get_current_weather(self, location):
        return await get_weather(location)

    async def search_google(self, keyword):
        return await search_google(keyword)


def image_generation(self, prompt: str) -> str:
    response = openai.images.generate(
        prompt=prompt,
        n=1,
        size=self.image_size
    )
    image_url = response.data[0].url
    return image_url
