import re
import sys
import time
import random

from rich.text import Text
from rich.live import Live
from rich.panel import Panel
from rich.align import Align
from rich.console import Console

from typing import Literal, Dict, List

from .chat_saver import save_chat, load_chat, load_keyword

console = Console()


def learn(response: str) -> None:
    """ Captures user prompts by simply saving it into json file memory"""
    pass


def tokenization(prompt: str) -> List:
    """ Seperating each word on the prompt """
    return re.findall(r"\w+|[^\w\s]", prompt.lower())


def identify_response(prompt: str, keywords: Dict = load_keyword()) -> str:
    """ this is where the bot choose a response """

    # stores memory.json data
    loaded_keywords: Dict = keywords

    for prompt_keyword in tokenization(prompt):
        for response, category_data in loaded_keywords.items():
            if prompt_keyword in category_data["keyword"]:
                return random.choice(category_data["response"])
    return random.choice(loaded_keywords["default"]["response"])


def generate_bot_response(prompt: str, prompter_name: str, bot_name: str) -> None:
    """ Definetly answers you 👌, but just randomly lmao. """

    print("\033[F\033[K", end='')

    generate_chat_head(
        role = "prompter",
        response = prompt,
        prompter_name = prompter_name,
        auto_save = True,
        file_name = "chat1.json"
    )

    generate_chat_head(
        role = "bot",
        response = identify_response(prompt),
        bot_name = bot_name,
        auto_save = True,
        file_name = "chat1.json",
        enable_typing_animation = True
    )


def generate_previous_chat_heads(file_name:str, prompter_name: str, bot_name: str) -> None:
     """ loads previous conversation of the chatbot and the prompter within the json file """
     for chat_head_response in load_chat(file_name):
        # * For chat head icons, getting the role type stored in between the squared brackets to identify the response ownership
        chat_head_icons_match = re.search(r"\[\s*(\w+)\s*\]\s*:", chat_head_response)

        # * For chat head response, getting the role type outside of the square bracket and semi colon, to get its response
        chat_head_response_match = re.search(r"\[\s*\w+\s*\]\s*:\s*(.*)", chat_head_response)

        if chat_head_icons_match and chat_head_response_match:
            generate_chat_head(
                role = chat_head_icons_match.group(1), 
                response = chat_head_response_match.group(1),
                prompter_name = prompter_name,
                bot_name = bot_name
            )


def typing_animation(prompt: str, duration: float = 0.05) -> None:
    """ just typing animation similar to chatgpt response """

    typed: List = Text("", style="bold magenta")

    with Live(console=console, refresh_per_second=20) as live:
        for char in prompt:
            typed.append(char)
            live.update(Panel.fit(typed, border_style="magenta"))
            time.sleep(duration) # How fast it will type 



def generate_chat_head(role: Literal["prompter", "bot"], response: str, prompter_name: str = "Haimonmon", bot_name: str = "Chad", auto_save: bool = False, file_name: str = None, enable_typing_animation: bool = False) -> None:
    if role not in ["prompter", "bot"]:
         print(f"[🐞] Invalid Role : {role}")
         return
    
    chat_head_icons: Dict = {
        "prompter": f"👑 {prompter_name}",
        "bot": f"🗿 {bot_name}"
    }

    chat_head_response: str = f"\n [ {chat_head_icons[role]} ] : {response} \n"
    chat_head_response_template: str = f"\n [ {role} ] : {response} \n"

    if auto_save:
        is_save = save_chat(file_name, chat_head_response_template)

        if not file_name:
            print(f"[🐞] Can't Identify the File name : {file_name}")
            return
        elif not is_save:
            print(f"[🐞] Failed to Save : {file_name}")
            return
    
    if role == "prompter":
        chat_head_text = Text(chat_head_response, style = "bold orange1")
        chat_head_panel = Panel.fit(chat_head_text, border_style="orange1")
        console.print(chat_head_panel, justify = "right")
    else:
        chat_head_text = Text(chat_head_response, style="bold magenta")
        chat_head_panel = Panel.fit(chat_head_text, border_style="magenta")

        if not enable_typing_animation:
            console.print(chat_head_panel, justify = "left")
        else:
            typing_animation(prompt = chat_head_response, duration = 0.03)

        
        

if __name__ == "__main__":
        # generate_chat_head(
        #     role = "prompter",
        #     response = "Bruh.",
        #     auto_save = True,
        #     file_name = "chat1.json"
        # )
        generate_previous_chat_heads("chat1.json")

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


