import json
import os
from typing import List, Dict, Literal
import openai
from openai._types import NotGiven, NOT_GIVEN
from openai.types.chat import ChatCompletionMessage, ChatCompletionToolChoiceOptionParam, ChatCompletionToolParam

from src.modelInterface import ModelInterface
from src.tools.google_search import search_google
from src.tools.open_weather import get_weather


class OpenAIModel(ModelInterface):
    def __init__(
            self,
            api_key: str,
            model_engine: str,
            image_model_engine: str,
            image_size: Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"] = '512x512'
    ):
        openai.api_key = api_key
        self.model_engine = model_engine
        self.image_model_engine = image_model_engine
        self.image_size = image_size

    async def chat_completion(self, messages: List[Dict] or ChatCompletionMessage) -> (str, str):
        tools = []

        if os.getenv("OPEN_WEATHER_API") is not None:
            tools.append({
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
            })

        if os.getenv("GOOGLE_CX") is not None and os.getenv("GOOGLE_SEARCH_API_KEY") is not None:
            tools.append({
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
            })

        tool_choices: ChatCompletionToolChoiceOptionParam or NotGiven = NOT_GIVEN

        if len(tools) > 0:
            tool_choices = 'auto'
        else:
            tools = NOT_GIVEN

        response = openai.chat.completions.create(
            model=self.model_engine,
            messages=messages,
            tool_choice=tool_choices,
            tools=tools
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            available_functions = {
                "get_current_weather": get_weather,
                "search_google": search_google
            }
            messages.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                if function_name == "get_current_weather":
                    function_response = await function_to_call(
                        city=function_args.get("location")
                    )
                elif function_name == "search_google":
                    function_response = await function_to_call(
                        keyword=function_args.get("keyword")
                    )
                else:
                    function_response = {}

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


def image_generation(self, prompt: str) -> str:
    response = openai.images.generate(
        model=self.image_model_engine,
        prompt=prompt,
        n=1,
        size=self.image_size
    )
    image_url = response.data[0].url
    return image_url
