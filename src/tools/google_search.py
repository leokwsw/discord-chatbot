import json
import os

import requests

from src.logger import logger


async def search_google(keyword: str):
    logger.log(level=0, msg=f"Searching Google with keyword {keyword}")
    query = keyword
    page = 1
    start = (page - 1) * 10 + 1
    url = f"https://www.googleapis.com/customsearch/v1?key={os.getenv('GOOGLE_SEARCH_API_KEY')}&cx={os.getenv('GOOGLE_CSE_ID')}&q={query}&start={start}"
    data = requests.get(url).json()
    search_items = data.get("items")

    result = []

    for i, search_item in enumerate(search_items, start=1):
        try:
            long_description = search_item["pagemap"]["metatags"][0]["og:description"]
        except KeyError:
            long_description = "N/A"
        title = search_item.get("title")
        snippet = search_item.get("snippet")
        html_snippet = search_item.get("htmlSnippet")
        link = search_item.get("link")
        result.append({
            "title": title,
            "description": snippet,
            "long description": long_description,
            "html_snippet": html_snippet,
            "link": link
        })
    return json.dumps(result)
