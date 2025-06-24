import os
import json

from typing import Dict, Literal

folder_directory = r"sigma/chats/"


def create_new_file(file_name) -> None:
    pass


def load_keyword() ->   None:
    """ loads keywords """

    with open("sigma/memory.json") as file:
        return json.load(file)


def load_chat(file: str) -> Dict:
    """ Loads previous chats """
    
    with open(f"{folder_directory}{file}", 'r') as file:
        return json.load(file)


def save_chat(file: str, response: str) -> bool:
    """ saves previous chats """

    if not file:
        return False
    
    try:
        loaded_chat_heads = load_chat(file)

        if not isinstance(loaded_chat_heads, list):
            print(f"[ Error ] The File doesnt contain a list")
            return False

        loaded_chat_heads.append(response)

        with open(f"{folder_directory}{file}", 'w') as file:
            json.dump(loaded_chat_heads, file, indent=4)

        return True
    except Exception as e:
        print(f"[ Error ] Something went wrong: {e}")
        return False


if __name__ == "__main__":
    save_chat("chat1.json", "Mah Kingsss for todayss 🔥🔥")

