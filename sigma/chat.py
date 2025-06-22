import time
import random

from pyfiglet import Figlet

from rich.panel import Panel
from rich.console import Console

from brain import generate_chat_head, generate_previous_chat_heads

console = Console()

def display_header(header_text: str, sub_header_text: str, title_header_text: str) -> None:
    """ pang displat lang ng header as introduction, can be either bot name, perfect with 5 letters maximum"""

    figlet = Figlet(font='alligator')
    logo = figlet.renderText(header_text)
    
    console.print(Panel.fit(f"[bold magenta] {logo} \n {"_" * 75} \n ✦ I dont know what im sayin, but im willing to answer 💀👌. [/bold magenta]", border_style = "magenta", title = title_header_text, padding=1))


def display_main_menu() -> None:
    """ display option """

    introduction_messages = [
        "Chat Ahead . . .   ",
        " Just hate being existed -_-",
        "Just ask bruhhh . . .   ",
        " Not a smart ass, just ask 👌"
    ]

    # generate_chat_head(role = "bot", response = random.choice(introduction_messages))
    generate_previous_chat_heads("chat1.json")
    console.input("[bold red] [ 👑 You ] [/] : ")


def sigma_bot(your_name: str = "Hitler") -> None:
    """ Landing Page """

    display_header("S | G M A", "* Just died from cringe *", "✦ Jet 2 Holiday ✦")
    display_main_menu()

if __name__ == "__main__":
      sigma_bot()

# TODO:
# ! Make sure the prompter will have a response always even before saving its chat head

# * References:
# * Rich Documentation: https: //rich.readthedocs.io/en/stable/console.html