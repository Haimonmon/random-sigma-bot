import time
import random

# * Our own chatbot library 🤙✨
import sigma as dizzy

# * External Libraries for Terminal style customization 🌾✨
from pyfiglet import Figlet

from rich.text import Text
from rich.live import Live
from rich.panel import Panel
from rich.console import Console

from typing import List, Dict, Literal

# * This will allow rich library to print its output on the console or terminal
console = Console()

def generate_bot_response(prompt: str, prompter_name: str, bot_name: str) -> None:
    """ 
    Displays chat heads of user prompt and bot response at the same time. 
    ```python
    (prompt: str) -> User prompt.
    (prompter_name: str) -> Prompter or user name.
    (bot_name: str) -> Name of the bot.
    ```
    """

    # * Move the "input" at the bottom of the chatheads
    print("\033[F\033[K", end='')

    # * Generates user prompt chat head
    generate_chat_head(
        role = "prompter",
        response = prompt,
        prompter_name = prompter_name,
    )

    # * Generates bot chat head with asking the chatbot for some response.
    generate_chat_head(
        role = "bot",
        response = dizzy.ask(prompt),
        bot_name = bot_name,
        enable_typing_animation = True
    )


def generate_previous_chats(file_name: str, prompter_name: str, bot_name: str) -> None:
    """
    loads previous conversation between the user and chatbot within the given json file.
    ```python
    (file_name: str) -> Json file name where the previous chat located.
    (prompter_name: str) -> Prompter or user name.
    (bot_name: str) -> Name of the bot.
    ```
    """

    # * Loads previous chat heads from the choosed json file.
    remembered_messages: List = dizzy.get_remembered_messages(file_name)

    for chat_head_response in remembered_messages:
        # * Checks if role and messages are not empty 
        if chat_head_response["role"] and chat_head_response["message"]:
            generate_chat_head(
                role = chat_head_response["role"],
                response = chat_head_response["message"],
                prompter_name = prompter_name,
                bot_name = bot_name
            )


def typing_animation(prompt: str, duration: float = 0.05) -> None:
    """ 
    just typing animation similar to chatgpt response.

    ```python
    (prompt: str) -> User prompt.
    (duration: float) -> You can change the typing speed.
    ```
    """

    typed: List = Text("", style="bold magenta")

    with Live(console=console, refresh_per_second=20) as live:
        for char in prompt:
            typed.append(char)
            live.update(Panel.fit(typed, border_style="magenta"))
            time.sleep(duration)  # * How fast it will type


def generate_chat_head(role: Literal["prompter", "bot"], response: str, prompter_name: str = "", bot_name: str = "", enable_typing_animation: bool = False) -> None:
    """
    Display single chat head for the given role.
    ```python
    (role: str) -> To identify chat heads ownership.
    (response: str) -> Message for the chat head, can be either chat response or user prompt.
    (prompter_name: str) -> Prompter or user name.
    (bot_name: str) -> Name of the bot.
    (enable_typing_animation: bool) -> Want to have the chat head generation a typing animation first?
    ```
    """
    # * Checks if role params have the given role, just making sure its just the "prompter" and the "bot" roles.
    if role not in ["prompter", "bot"]:
        print(f"[🐞] Invalid Role : {role}")
        return

    chat_head_icons: Dict = {
        "prompter": f"👑 {prompter_name}",
        "bot": f"🗿 {bot_name}"
    }

    chat_head_response: str = f"\n [ {chat_head_icons[role]} ] : {response} \n"

    # * Each roles need to have unique color chat heads.
    if role == "prompter":
        chat_head_text = Text(chat_head_response, style="bold orange1")
        chat_head_panel = Panel.fit(chat_head_text, border_style="orange1")
        console.print(chat_head_panel, justify="right")
    else:
        chat_head_text = Text(chat_head_response, style="bold magenta")
        chat_head_panel = Panel.fit(chat_head_text, border_style="magenta")

        if not enable_typing_animation:
            console.print(chat_head_panel, justify="left")
        else:
            typing_animation(prompt=chat_head_response, duration=0.03)


def display_header(header_text: str, sub_header_text: str, title_header_text: str) -> None:
    """ 
    pang display lang ng header as introduction, can be either bot name, perfect with 5 letters maximum 

    ```python
    (header_text: str) -> Large text to be shown up.
    (sub_header_text: str) -> Mini text below of the header text.
    (title_header: str) -> mini title along with the header border or panel.
    ```
    """

    figlet = Figlet(font='alligator')
    logo = figlet.renderText(header_text)
    line_separator = "_" * 75
    
    # * Example of rich library own print() function.
    console.print(Panel.fit(f"[bold magenta] {logo} \n {line_separator} \n {sub_header_text} [/bold magenta]", border_style = "magenta", title = title_header_text, padding=1), justify = "center")


def display_chat_window(prompter_name: str, bot_name: str, selected_chat_session: str) -> None:
    """ 
    Display prompter and bot chat heads and a section to type the prompt 

    ```python
    (prompter_name: str) -> choose any name you want for you, same as user name
    (bot_name: str) -> Allow bot name customization
    (selected_chat_session) -> chooses a certain chat session to start of the conversation
    ```
    """

    chat_session: List = dizzy.get_remembered_messages(selected_chat_session)

    # * Making sure previous chats will be loaded once the bot started.
    is_previous_chat_loaded: bool = False

    while True:
        # * Once the chats json doesnt have any data on its list, it will be a hint for a New chat session.
        if len(chat_session) == 0:
            # * Pick greeting response as starting default
            greeting_response = random.choice(dizzy.get_knowledge()["greetings"]["response"])

            # * Save greeting response to the selected chat session or json file
            dizzy.remember_message(selected_chat_session, role = "bot", message = greeting_response)

            # * Once its a new chat session, the prompter will be greeted with the bot message.
            generate_chat_head(
                role = "bot",
                response = greeting_response,
                bot_name = bot_name,
                enable_typing_animation = True
            )

            # * Make sure to add the latest chat with the greetings to avoid unlatest data.
            chat_session: List = dizzy.get_remembered_messages(selected_chat_session)
            is_previous_chat_loaded: bool = True
            
        elif len(chat_session) != 0 and not is_previous_chat_loaded:
            generate_previous_chats(
                file_name = selected_chat_session, 
                prompter_name = prompter_name, 
                bot_name = bot_name
            )

            # * Change status to load chat session data once only.
            is_previous_chat_loaded: bool = True
       
        prompt: str = console.input("[bold orange1] [ 👑 You ] [/] : ")

        # * This is where the chat bot response to user prompt.
        generate_bot_response(
            prompt = prompt, 
            prompter_name = prompter_name, 
            bot_name = bot_name
        )

        # * Exit detection of chat session.
        if say_goodbye(prompt):
            break


def say_goodbye(prompt: str) -> bool:
    """ 
    Make sure the user says a goodbye to its best friend 
    """
    for keyword in dizzy.tokenization(prompt):
        if keyword in dizzy.get_knowledge()["farewell"]["keyword"]:
            return True
    return False
    
    
def sigma_bot(your_name: str = "You", bot_name = "Dizzy") -> None:
    """ 
    The main of the bot application
    ```python
    (your_name: str) -> Pangalan molang.
    (bot_name: str) -> Bot name basta hahaha.
    ```
    """

    # * Display a panel pane with the bot name at the start of the program.
    display_header(
        header_text = "D | Z Z Y", 
        sub_header_text = "✦ I dont know what im sayin, but im willing to answer 💀👌.", 
        title_header_text = "✦ Jet 2 Holiday ✦"
    )

    # * Display the chat window where chat heads of prompter and bot are in.
    display_chat_window(
        prompter_name = your_name ,
        bot_name = bot_name, 
        selected_chat_session = "chat1.json"
    )

if __name__ == "__main__":
      sigma_bot()

# TODO:
# ! Make sure the prompter will have a response always even before saving its chat head
# ! Make sure to have a Automatic Text wrap on each chat heads
# ! Add loading screen for startup and prompt bot delay response
# ! use levenshtein algorithm for keyword mispelled

# * References:
# * Rich Documentation: https: //rich.readthedocs.io/en/stable/console.html