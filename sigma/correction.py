import re
import math

from typing import List, Dict, Any

from .memory import get_knowledge

def tokenization(prompt: str) -> List:
    """ Seperating each word of the prompt """
    return re.findall(r"[a-zA-Z0-9']+|[.,!?;]", prompt.lower())


def levenshtein(keyword1: str, keyword2: str) -> int:
    """
    A function that scales the misspelled words wrongness.
    """
    len1 = len(keyword1)
    len2 = len(keyword2)

    dp = [[0] * (len2 + 1) for x in range(len1 + 1)]

    for i in range(len1 + 1):
        for j in range(len2 + 1):

            if i == 0:
                dp[i][j] = j

            elif j == 0:
                dp[i][j] = i

            elif keyword1[i-1] == keyword2[j-1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])

    return dp[len1][len2]


def fuzzy_matching(keyword1: str, keyword2: str) -> float:
    """ Compares the similiraties between the two words given by levenshtein """
    distance = levenshtein(keyword1=keyword1, keyword2=keyword2)
    score = 1 - (distance / max(len(keyword1), len(keyword2)))
    return round(score, 2)


def jaccard_similarity(a: str, b: str) -> float:
    """ Compares the similiraties between the two words given by levenshtein"""
    set_a = set(a)
    set_b = set(b)
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def hybrid_score(a: str, b: str) -> float:
    """ Both jaccard and levenshtein based distancing or scoring """
    lev = fuzzy_matching(a, b)
    jac = jaccard_similarity(a, b)
    return round((lev + jac) / 2, 2)


def best_match(word: str, choices: List["str"], threshhold: float = 0.75) -> str:
    """ identifies whats the best match on the given word with the given list of choices with possible matches """
    if word in choices:
        return word

    best_match = None
    best_score = -1

    for option in choices:
        score = hybrid_score(word, option)
        if score > best_score:
            best_match = option
            best_score = score
            # print(best_match, option, best_score)
        # elif score == best_score:
        #     if option < best_match:
        #         best_match = option

    return best_match if best_score >= threshhold else None


def split_word(word: str, keywords: List[str]) -> None:
    """ Splits jumbled words with the help of given keywords """
    if word in keywords:
        return [word]

    for i in range(1, len(word)):
        left = word[:i]
        right = word[i:]

        if left in keywords:
            rest_split = split_word(right, keywords)
            if rest_split:
                return [left] + rest_split

    return None


def check_keyword(word: str, keywords: List[str]) -> None:
    for kw in keywords:
        if " " in kw:
            tokenized_keyword = tokenization(kw)

            split = split_word(word, tokenized_keyword)

            if split:
                return split

    return None


def normalize_prompt(prompt: str, knowledge: Dict[str, List[str]]) -> List[str]:
    """ Automatically tokenizes and normalizes jumbled/misspelled words """
    tokens: List[str] = tokenization(prompt)
    keywords: List[str] = join_keywords(knowledge)    
    normalized = []
  
    for word in tokens:
        if word in keywords:
            normalized.append(word)
            continue

        word_splitted = split_word(word, keywords)
        word_mispelled = best_match(word, keywords)
        phrase_check = check_keyword(word, keywords)

        if phrase_check:
            normalized.extend(phrase_check)
            continue

        if word_splitted:
            normalized.extend(word_splitted)
            continue

        if word_mispelled:
            normalized.append(word_mispelled)
            continue

    return normalized


def join_keywords(knowledge: Dict[str, List[str]]) -> List[str]:
    """ Joins all of the keywords known in greets.json into one Array """
    seen = set()
    combined = []

    for category_data in knowledge.values():
        for keyword in category_data["keyword"]:
            if keyword not in seen:
                combined.append(keyword)
                seen.add(keyword)
    
    almanac: Dict[str, Any] = get_knowledge("almanac.json")
    combined = list(seen.union(almanac.keys()))

    return combined


if __name__ == "__main__":
    prompt: str = "i love yi so mich"
    
