import re
import random
from typing import Dict, List
from .memory import remember_message, get_knowledge
from .emotion import detect_emotion, is_question, detect_list_request, get_emotion_keywords

# Common English words, this will use to prevent the getting the common words as possible typos (for debugging anyway or for future purposes like edit distance)
common_words = {
    "i", "im", "am", "and", "so", "about", "you", "your", "my", "me", "we", "us", "the", "a", "an", "to", "in", "on",
    "for", "of", "is", "are", "it", "this", "that", "be", "with", "at", "as", "was", "were", "have", "has", "do",
    "does", "not", "but", "or", "if", "because", "then", "than", "too", "very", "just", "much", "more", "any"
}

# Tokenizer
def tokenization(prompt: str) -> List[str]:
    return re.findall(r"\w+|[^\w\s]", prompt.lower())

# It will detect typos (by checking if each word exists in this set) also to avoid false positives on common words like "i", "and", "so"
def extract_dictionary_words(knowledge: Dict) -> set:
    extracted = set()
    for category in knowledge.values():
        extracted.update(category.get("keyword", []))
    return extracted | common_words | get_emotion_keywords()

# Basic spell check
def basic_spellcheck(word: str, dictionary_words: set) -> bool:
    return word in dictionary_words

# Optional: learning module stub
def learn(response: str, file="learned.json") -> None:
    tokens = tokenization(response)
    unknown = [word for word in tokens if word not in extract_dictionary_words(get_knowledge())]
    if unknown:
        entry = {
            "message": response,
            "suggested_keywords": unknown
        }
        remember_message(file, role="learn", message=entry)

# Main logic
def ask(prompt: str, knowledge: Dict = get_knowledge(), file="chat1.json", remember: bool = True) -> str:
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
        is_save = remember_message(file, role="prompter", message=prompt)
        if not file or not is_save:
            print(f"[🐞] Can't identify or save to file: {file}")
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

    if "greetings" in category_responses:
        response_parts.append(category_responses["greetings"])
    
    if "genz_slang" in category_responses:
        response_parts.append(f"You’re speaking fluent Gen Z 🔥 {category_responses['genz_slang']}")

    if "compliments" in category_responses and "objects" in category_responses:
        objects_mentioned = [w for w in tokens if w in knowledge["objects"]["keyword"]]
        response_parts.append(f"It's lovely you’re into {', '.join(objects_mentioned)} — {category_responses['objects']}")
        response_parts.append(category_responses["compliments"])
    elif "compliments" in category_responses:
        response_parts.append(category_responses["compliments"])
    elif "objects" in category_responses:
        objects_mentioned = [w for w in tokens if w in knowledge["objects"]["keyword"]]
        response_parts.append(f"Ah, {', '.join(objects_mentioned)} — {category_responses['objects']}")

    if "places" in category_responses:
        response_parts.append(category_responses["places"])

    if "farewell" in category_responses:
        response_parts.append(category_responses["farewell"])

    if "default" in category_responses:
        response_parts.append(category_responses["default"])

    final_response = " ".join(response_parts)
    
    # this part is for debugging only for checking if the logic is correct 
    final_response += f"\n🙂 Emotion: {emotion}"
    if question:
        final_response += " | ❓ Question detected"
    if wants_list:
        final_response += " | 📋 List intent"
    if misspelled:
        final_response += f" | 🛑 Possible typos: {', '.join(misspelled)}"

    if remember:
        remember_message(file=file, role="bot", message=final_response)

    return final_response

# Dev test
if __name__ == "__main__":
    print(ask("hello im cathy, and i love so much about flowers"))


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


