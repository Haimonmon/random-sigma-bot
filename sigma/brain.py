import re
import random
from typing import Dict, List
from .memory import remember_message, get_knowledge, add_knowledge
from .emotion import detect_emotion, is_question, detect_list_request, get_emotion_keywords

common_words = {
    "i", "im", "am", "and", "so", "about", "you", "your", "my", "me", "we", "us", "the", "a", "an", "to", "in", "on",
    "for", "of", "is", "are", "it", "this", "that", "be", "with", "at", "as", "was", "were", "have", "has", "do",
    "does", "not", "but", "or", "if", "because", "then", "than", "too", "very", "just", "much", "more", "any"
}

def tokenization(prompt: str) -> List:
    """ Seperating each word of the prompt """
    return re.findall(r"[a-zA-Z0-9']+|[.,!?;]", prompt.lower())


def extract_dictionary_words(knowledge: Dict) -> set:
    """ It will detect typos (by checking if each word exists in this set) also to avoid false positives on common words like "i", "and", "so" """
    extracted = set()
    for category in knowledge.values():
        extracted.update(category.get("keyword", []))
    return extracted | common_words | get_emotion_keywords()


def basic_spellcheck(word: str, dictionary_words: set) -> bool:
    """ Basic spell check """
    return word in dictionary_words


def learn(response: str) -> None:
    """
    Captures user prompts by simply saving it into json file memory

    (response: str) -> User prompt.
    """
    tokens = tokenization(response)
    unknown = [word for word in tokens if word not in extract_dictionary_words(get_knowledge())]
    if unknown:
        entry = {
            "message": response,
            "suggested_keywords": unknown
        }
        add_knowledge(file_name = "learned.json", info = entry)


def ask(prompt: str, knowledge: Dict = get_knowledge(file_name = "greets.json"), file="chat1.json", remember: bool = True, debug_mode: bool = False) -> str:
    """
    Ask the bot any question and it will answer thruthfully.. i guess..

    ```python
    (prompt: str) -> User prompt.
    (knowledge: Dict) -> Contains keywords known by the bot.
    (file: str) -> Contains the file name for saving user and bot responses.
    (remember: bool) -> Enable the bot to save user and bot responses.
    ```
    """
    # Tokenize the input prompt into words/symbols
    tokens = tokenization(prompt)
    dictionary_words = extract_dictionary_words(knowledge)

    # it will initialize match and response containers
    matched_categories = []
    category_responses = {}

    # It will analyze prompt emotion, check if it's a question, list request, or contains misspellings
    emotion = detect_emotion(tokens)
    question = is_question(tokens, prompt)
    wants_list = detect_list_request(tokens)

    misspelled = [w for w in tokens if not basic_spellcheck(w, dictionary_words) and w.isalpha()]

    if remember:
        is_save = remember_message(file_name = file, role="prompter", message=prompt)
        if not file or not is_save:
            print(f"[ 🐞 ] Can't identify or save to file: {file}")
            return
        elif not is_save:
            print(f"[🐞] Failed to Save : {file}")
            return

    # Match responses by category and randomize the response.
    
    for category, data in knowledge.items():
        if any(keyword in tokens for keyword in data.get("keyword", [])):
            matched_categories.append(category)
            category_responses[category] = random.choice(data["response"])

    # Use default if nothing matched
    if not category_responses and "default" in knowledge:
        matched_categories.append("default")
        category_responses["default"] = random.choice(knowledge["default"]["response"])

    # This chunk of code will create or construct a smart response
    response_parts = []

    # print(category_responses)
    if "greetings" in category_responses:
        response_parts.append(category_responses["greetings"])

    if "genz_slang" in category_responses:
        response_parts.append(f"You're speaking fluent Gen Z 🔥 {category_responses['genz_slang']}")
    
    if "interrogative" in category_responses:
        response_parts.append(f"\n {category_responses["interrogative"]}")
        response_parts.append(f"\n {random.choice(get_knowledge(file_name = "almanac.json")[identify_entity(prompt)]["answers"])}")
        
        
    if "compliments" in category_responses and "objects" in category_responses:
        objects_mentioned = [w for w in tokens if w in knowledge["objects"]["keyword"]]
        response_parts.append(f"It's lovely you're into {', '.join(objects_mentioned)} - {category_responses['objects']}")
        response_parts.append(category_responses["compliments"])
    elif "compliments" in category_responses:
        response_parts.append(category_responses["compliments"])
    elif "objects" in category_responses:
        objects_mentioned = [w for w in tokens if w in knowledge["objects"]["keyword"]]
        response_parts.append(f"Ah, {', '.join(objects_mentioned)} - {category_responses['objects']}")

    if "places" in category_responses:
        response_parts.append(category_responses["places"])

    if "farewell" in category_responses:
        response_parts.append(category_responses["farewell"])

    if "default" in category_responses:
        response_parts.append(category_responses["default"])

    final_response = " ".join(response_parts)
  
    # this part is for debugging only for checking if the logic is correct
    if debug_mode:
        final_response += f"\n🙂 Emotion: {emotion}"
        if question:
            final_response += " | ❓ Question detected"
        if wants_list:
            final_response += " | 📋 List intent"
        if misspelled:
            final_response += f" | 🛑 Possible typos: {', '.join(misspelled)}"

    if remember:
        remember_message(file_name = file, role="bot", message=final_response)

    return final_response


def levenshtein(keyword1: str, keyword2: str) -> int:
    """
    A function that scales the misspelled words wrongness.
    """
    pass


# * ========================================================================= ask question
def identify_entity(prompt: str) -> None:
    tokens = tokenization(prompt)
    almanac = get_knowledge(file_name="almanac.json")

    # print("[🧠] Tokens:", tokens)

    best_match = None
    best_score = 0

    for key, data in almanac.items():
        score = 0
        for keyword in data["keywords"]:
            keyword_tokens = tokenization(keyword)
            if all(word in tokens for word in keyword_tokens):
                # print(keyword, keyword_tokens)
                score += 1  # +1 per matched keyword

        if score > best_score:
            best_score = score
            best_match = key
            # print(f"[🔥] '{key}' scored {score} points")


    return best_match or "no answer"


if __name__ == "__main__":
        # print(ask_question("Can you breakdown for me, what is rizz?"))
        # print(identify_entity("whats up"))
        pass
       
        
       
        # TODO: required bot iNteractions:
        # responds to a list, like asking for recipee, best places
        # enable to identify, places, object
        # our bot enable to learn by capturing user sentences
        # able to identify mispelled words
        # can have an emotions and identify emotions by sentiment analysis

        # TODO: Bug occurence
        # ! Fix Bug "see ya" in keywords (json data) is different from "see" , "ya" when tokenized the user prompt, 


       

