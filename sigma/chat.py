import time
import random

from typing import List

from pyfiglet import Figlet

from rich.panel import Panel
from rich.console import Console

from .chat_saver import load_chat, load_keyword
from .brain import generate_chat_head, generate_previous_chat_heads, generate_bot_response

console = Console()

def display_header(header_text: str, sub_header_text: str, title_header_text: str) -> None:
    """ pang displat lang ng header as introduction, can be either bot name, perfect with 5 letters maximum"""

    figlet = Figlet(font='alligator')
    logo = figlet.renderText(header_text)
    line_separator = "_" * 75
    
    console.print(Panel.fit(f"[bold magenta] {logo} \n {line_separator} \n {sub_header_text} [/bold magenta]", border_style = "magenta", title = title_header_text, padding=1))


def display_chat_session(prompter_name, bot_name, selected_chat_session: str) -> None:
    """ display option """

    # * For a while 
    introduction_messages = [
        "Chat Ahead . . .   ",
        " Just hate being existed -_-",
        "Just ask bruhhh . . .   ",
        " Not a smart ass, just ask 👌"
    ]

    chat_session: List = load_chat(selected_chat_session)
    is_previous_chat_loaded: bool = False

    while True:
        if len(chat_session) == 0:
            generate_chat_head(
                role = "bot",
                response = random.choice(introduction_messages),
                bot_name = bot_name,
                auto_save = True,
                file_name = selected_chat_session
            )

            chat_session: List = load_chat(selected_chat_session)
        elif len(chat_session) != 0 and not is_previous_chat_loaded:
            generate_previous_chat_heads(file_name = selected_chat_session)
            is_previous_chat_loaded: bool = True
       
        response: str = console.input("[bold orange1] [ 👑 You ] [/] : ")

        generate_bot_response(prompt = response)

        if response in load_keyword()["farewell"]["keyword"]:
            break


def sigma_bot(your_name: str = "Hitler", bot_name = "Chad") -> None:
    """ Landing Page """

    display_header(
        header_text = "l | G M A", 
        sub_header_text = "✦ I dont know what im sayin, but im willing to answer 💀👌.", 
        title_header_text = "✦ Jet 2 Holiday ✦"
    )

    display_chat_session(prompter_name = your_name ,bot_name = bot_name, selected_chat_session = "chat1.json")

if __name__ == "__main__":
      sigma_bot()

# TODO:
# ! Make sure the prompter will have a response always even before saving its chat head
# ! Make sure to have a Automatic Text wrap on each chat heads
# ! Make the prompter chat heads on the right side while bot chat heads is on the left
# ! Make all of the components on center
# ! Add loading screen for startup and prompt bot delay response

# * References:
# * Rich Documentation: https: //rich.readthedocs.io/en/stable/console.html