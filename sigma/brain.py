import re
import random

from typing import Dict, List
from .correction import normalize_prompt, tokenization
from .learn import know_prompter_name, remember_message, get_knowledge
from .emotion import detect_emotion, is_question, detect_list_request, get_emotion_keywords

# common_words = {
#     "i", "im", "am", "and", "so", "about", "you", "your", "my", "me", "we", "us", "the", "a", "an", "to", "in", "on",
#     "for", "of", "is", "are", "it", "this", "that", "be", "with", "at", "as", "was", "were", "have", "has", "do",
#     "does", "not", "but", "or", "if", "because", "then", "than", "too", "very", "just", "much", "more", "any"
# }


is_goodbye = False

def is_end_conversation() -> bool:
    return is_goodbye


def ask(prompt: str, knowledge: Dict = get_knowledge(file_name = "greets.json"), file="chat1.json", remember: bool = True, debug_mode: bool = False) -> str:
    global is_goodbye
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
    tokens = normalize_prompt(prompt = prompt, knowledge = knowledge)

    # it will initialize match and response containers
    category_score = {}
    matched_categories = []
    category_responses = {}

    if remember:
        is_save = remember_message(file_name = file, role="prompter", message=prompt)
        if not file or not is_save:
            print(f"[ 🐞 ] Can't identify or save to file: {file}")
            return
        elif not is_save:
            print(f"[🐞] Failed to Save : {file}")
            return

    # Match responses by category and randomize the response.
    # print(tokens)
    for category, data in knowledge.items():
        for keyword in data["keyword"]:
            if keyword_in_tokens(keyword, tokens):
                # * increment score for each match
                category_score[category] = category_score.get(category, 0) + 1
                # print(category, keyword)

                # * add matched category once
                if category not in matched_categories:
                    matched_categories.append(category)

                # * pick a random response (only once)
                if category not in category_responses:
                    category_responses[category] = random.choice(data["response"])

    # * Use default if nothing matched
    if not category_responses and "default" in knowledge:
        matched_categories.append("default")
        category_responses["default"] = random.choice(knowledge["default"]["response"])

    response_parts = []

    # print(category_responses)
    # print(category_score)

    # * Prioritize knowing the user
    if "identity_name" in category_responses:
        name = know_prompter_name(prompt)
        if name:
            response_parts.append(category_responses["identity_name"].replace("{name}", name))
        else:
            response_parts.append("hmmm sorry what?, i cant specify your name 😗")

    if "identity_name" not in category_responses:
        if "greetings" in category_responses:
            response_parts.append(category_responses["greetings"])

        if "genz_slang" in category_responses:
            response_parts.append(f"You're speaking fluent Gen Z 🔥 {category_responses['genz_slang']}")
        
        if "interrogative" in category_responses:
            response_parts.append(f"\n {category_responses["interrogative"]}")
            response_parts.append(f"\n {random.choice(get_knowledge(file_name = "almanac.json")[identify_entity(tokens)]["answers"])}")
            
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

        if "farewell" in category_responses and list(category_responses.keys()) == ["farewell"]:
            response_parts.append(category_responses["farewell"])
            is_goodbye = True

        if "positive" in category_responses:
            response_parts.append(category_responses["positive"])
        
        if "negative"in category_responses:
            response_parts.append(category_responses["negative"])

        if "default" in category_responses:
            response_parts.append(category_responses["default"])

    final_response = " ".join(response_parts)
  
    # this part is for debugging only for checking if the logic is correct
    # if debug_mode:
    #     final_response += f"\n🙂 Emotion: {emotion}"
    #     if question:
    #         final_response += " | ❓ Question detected"
    #     if wants_list:
    #         final_response += " | 📋 List intent"
    #     if misspelled:
    #         final_response += f" | 🛑 Possible typos: {', '.join(misspelled)}"

    if remember:
        remember_message(file_name = file, role="bot", message = final_response)

 
    return final_response


def normalize_tokens(tokens: List[str]) -> List[str]:
    normalized = []
    for token in tokens:
        normalized.extend(tokenization(token))
    return normalized


def keyword_in_tokens(keyword: str, tokens: List[str]) -> bool:
    keyword_tokens = tokenization(keyword)
    flat_tokens = normalize_tokens(tokens)

    # if len(keyword_tokens) > 1:
    #     print(keyword_tokens, flat_tokens)

    for i in range(len(flat_tokens) - len(keyword_tokens) + 1):
        if flat_tokens[i:i + len(keyword_tokens)] == keyword_tokens:
            return True
    return False


# * ========================================================================= ask question
def identify_entity(tokens: str) -> None:
    almanac = get_knowledge(file_name="almanac.json")

    # print("[🧠] Tokens:", tokens)

    best_match = None
    best_score = 0

    for key, data in almanac.items():
        score = 0
        for keyword in data["keyword"]:
            keyword_tokens = tokenization(keyword)
            # print(tokens)
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


       

