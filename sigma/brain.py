import re
import random

from typing import Dict, List

from .memory import remember_message, get_remembered_messages, get_knowledge

def learn(response: str) -> None:
    """ 
    Captures user prompts by simply saving it into json file memory

    (response: str) -> User prompt.
    """
    pass


def tokenization(prompt: str) -> List:
    """ Seperating each word of the prompt """
    return re.findall(r"\w+|[^\w\s]", prompt.lower())


def ask(prompt: str, knowledge: Dict = get_knowledge(), file = "chat1.json", remember: bool = True) -> str:
    """ 
    Ask the bot any question and it will answer thruthfully.. i guess..

    ```python
    (prompt: str) -> User prompt.
    (knowledge: Dict) -> Contains keywords known by the bot.
    (file: str) -> Contains the file name for saving user and bot responses.
    (remember: bool) -> Enable the bot to save user and bot responses.
    ```
    """

    # * stores memory.json data
    loaded_knowledge: Dict = knowledge

    # * Saves user prompt on specific json file
    if remember:
        is_save = remember_message(file, role="prompter", message=prompt)

        if not file:
            print(f"[🐞] Can't Identify the File name : {file}")
            return
        elif not is_save:
            print(f"[🐞] Failed to Save : {file}")
            return
        
    for prompt_keyword in tokenization(prompt):
        for response, category_data in loaded_knowledge.items():
            if prompt_keyword in category_data["keyword"]:

                # * Saves bot response on json file
                response = random.choice(category_data["response"])
                if remember:
                    remember_message(file_name = file, role = "bot", message = response)
                return response
    
    # * Saves bot default response on json file
    default_response: str = random.choice(category_data["response"])
    if remember:
        remember_message(file_name = file, role = "bot", message = default_response)
    return default_response
        

def levenshtein(keyword1: str, keyword2: str) -> int:
    """
    A function that scales the misspelled words wrongness.
    """
    pass

if __name__ == "__main__":
        ask("hello")

        # TODO: required bot iNteractions:
        # responds to a list, like asking for recipee, best places
        # enable to identify, places, object
        # our bot enable to learn by capturing user sentences
        # able to identify mispelled words
        # can have an emotions and identify emotions by sentiment analysis
        # aBle to identify questions


       

