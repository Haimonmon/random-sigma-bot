import re
import aiohttp
import asyncio
import requests

from typing import List, Dict

from .memory import remember_message, get_knowledge, add_knowledge
from .correction import tokenization, join_keywords


def is_name(tokenized_prompt: List[str]) -> None:
    """ Checks if the word exist on vocab """
    knowledge: Dict = get_knowledge("greets.json")
    combined_keywords: List[str] = join_keywords(knowledge)

    detected_name: str = None

    for prompt in tokenization(tokenized_prompt):
        if prompt in combined_keywords:
            continue
        
        detected_name = prompt

    return detected_name
        

def know_prompter_name(tokenized_prompt: List[str]) -> str:
    """ Remember user name """
    prompter_info: Dict = get_knowledge("prompter_info.json")

    name = is_name(tokenized_prompt)

    if name:
        prompter_info["name"] = name
        add_knowledge("prompter_info.json", info = prompter_info)
    
    # print("tokenzied: ", name)
    return name


def know_prompter_likes() -> None:
    pass


if __name__ == "__main__":
    sentence: str = ""

    print(know_prompter_name(tokenized_prompt = tokenization("Im ")))