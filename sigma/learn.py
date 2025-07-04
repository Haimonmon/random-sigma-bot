import re
import aiohttp
import asyncio
import requests

from typing import List, Dict

from .memory import remember_message, get_knowledge, add_knowledge
from .correction import tokenization


def get_online_data(word: str) -> List:
    """ gets the word meaning and pos from online api"""
    url_dictionary_link = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"

    try:
        response = requests.get(url_dictionary_link)

        if response.status_code != 200:
            return None

        return response.json()
    except Exception as e:
        return None


def learn_prompt_pos(prompt: str) -> None:
    """ learn each words on the sentence by their parts of speech """
    token: List = tokenization(prompt=prompt)
    learned_word: Dict = get_knowledge(file_name="pos.json")

    if "not_defined" not in learned_word:
        learned_word["not_defined"] = []

    for word in token:
        if word not in learned_word:
            if word in ['.',';',':','!','?',',']:
                continue

            dictionary = get_online_data(word = word)
            learned_word[word] = []

            if not dictionary and word not in learned_word["not_defined"]:
                learned_word["not_defined"].append(word)
                continue
            
            for data in dictionary:
                for meaning in data["meanings"]:
                    if meaning["partOfSpeech"] not in learned_word[word]:
                        learned_word[word].append(meaning["partOfSpeech"])

    add_knowledge(file_name = "pos.json", info = learned_word)


def learn_word(word) -> str:
    pass


if __name__ == "__main__":
    sentence: str = ""

    learn_prompt_pos(prompt = sentence)



