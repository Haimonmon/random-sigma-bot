import os
import json

from typing import Dict, Literal, List

folder_directory = r"sigma/chats/"


def create_new_file(file_name) -> None:
    pass


def get_knowledge() -> Dict:
    """ loads keywords """

    with open("sigma/knowledge.json", "r", encoding="utf-8") as file:
        return json.load(file)


def get_remembered_messages(file: str) -> List:
    """ Loads previous chats """
    
    with open(f"{folder_directory}{file}", 'r') as file:
        return json.load(file)


def remember_message(file: str, role: Literal["prompter", "bot"], message: str) -> bool:
    """ it remembers what you say earlier """

    if not file:
        return False
    
    try:
        # * Loaded json file from chats
        remembered_messages: List = get_remembered_messages(file)

        if not isinstance(remembered_messages, list):
            print(f"[ Error ] The File doesnt contain a list")
            return False

        remembered_messages.append({"role": role, "message": message})

        with open(f"{folder_directory}{file}", 'w') as file:
            json.dump(remembered_messages, file, indent = 4)

        return True
    except Exception as e:
        print(f"[ Error ] Something went wrong: {e}")
        return False


if __name__ == "__main__":
    remember_message("chat1.json", "bot", "Mah Kingsss for todayss 🔥🔥")

