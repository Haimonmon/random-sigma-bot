import re
import sys
import time
import random


from typing import Dict, List

from .memory import remember_message, get_remembered_messages, get_knowledge

def learn(response: str) -> None:
    """ Captures user prompts by simply saving it into json file memory"""
    pass


def tokenization(prompt: str) -> List:
    """ Seperating each word on the prompt """
    return re.findall(r"\w+|[^\w\s]", prompt.lower())


def ask(prompt: str, knowledge: Dict = get_knowledge(), file = "chat1.json", remember: bool = True) -> str:
    """ 
    this is where the dizzy bot choose a response 
    """

    # * stores memory.json data
    loaded_knowledge: Dict = knowledge

    # * Saves user asked prompt on specific json file
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
                    remember_message(file = file, role = "bot", message = response)
                return response
    
    # * Saves bot default response on json file
    default_response: str = random.choice(category_data["response"])
    if remember:
        remember_message(file = file, role = "bot", message = default_response)
    return default_response
        

if __name__ == "__main__":
        ask("hello")

        # TODO: required bot iNteractions:
        # responds to a list, like asking for recipee, best places
        # enable to identify, places, object
        # our bot enable to learn by capturing user sentences
        # able to identify mispelled words
        # can have an emotions and identify emotions by sentiment analysis
        # aBle to identify questions


        """
        since we have a category for each keywords and responses we can base the user prompt 
        how much his sentence are based off on those category.

        for example:
        
        "hello im cathy, and i love so much about flowers "

        hello word are in the greetings category

        love are in compliment category

        flowers are in object category

        """


