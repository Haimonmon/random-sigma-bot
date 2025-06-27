import os
import json

from typing import Dict, Literal, List, Any

folder_directory = r"sigma/chats/"


def create_new_file(file_name) -> None:
    pass

def load_file(file_name: str) -> List:
    """ Loads data on the specified json file name. """
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)


def save_file(file_name: str, data: Any) -> None:
    """ Saves data on the specified json file name. """
    with open(file_name, 'w') as file:
        json.dump(data, file, indent = 4)


def get_knowledge(file_name: Literal["greets.json", "almanac.json", "interrogatives.json"]) -> Dict:
    """ loads known keywords and responses from the knowledge folder """
    return load_file(file_name = f"sigma/knowledge/{file_name}")


def get_remembered_messages(file_name: str) -> List:
    """ Loads previous known chats """
    return load_file(file_name = f"{folder_directory}{file_name}")


def remember_message(file_name: str, role: Literal["prompter", "bot"], message: str) -> bool:
    """ 
    Saves a specific message on the given json file

    ```python
    (file_name: str) -> Contains the specific json file name to save
    (role: str) -> Contains two roles only, prompter, bot.
    (message: str) -> prompt or either bot response can be remembered or save
    ```
    """
    if not file_name:
        return False
    
    try:
        # * Loaded json file from chats
        remembered_messages: List = get_remembered_messages(file_name)

        # * Just make sure the file have a list, if not, it will create its own empty list.
        if not isinstance(remembered_messages, list):
            print(f"[ Caution ] The File doesnt contain a list")
            save_file(file_name = f"{folder_directory}{file_name}", data = [])
            
        # * Adds the data on the remembered messages loaded
        remembered_messages.append({"role": role, "message": message})

        # * Saves message on the loaded remembered messsages loaded
        save_file(file_name = f"{folder_directory}{file_name}", data = remembered_messages)
        return True
    except Exception as e:
        print(f"[ Error ] Something went wrong: {e}")
        return False


if __name__ == "__main__":
    remember_message(
        file = "chat1.json", 
        role = "bot", 
        message = "Mah Kingsss for todayss 🔥🔥"
    )

