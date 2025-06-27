# Base keyword groups for checking the category in knowledge.json
positive_words = {"love", "like", "enjoy", "amazing", "great", "awesome", "nice"}
negative_words = {"hate", "dislike", "boring", "bad", "terrible", "annoying"}
question_words = {"who", "what", "where", "when", "why", "how"}
list_keywords = {"list", "top", "best", "recommend", "recipe", "suggest"}

# Detect basic sentiment
def detect_emotion(tokens):
    score = sum(1 for t in tokens if t in positive_words) - sum(1 for t in tokens if t in negative_words)
    if score > 0:
        return "🙂 Positive"
    elif score < 0:
        return "☹️ Negative"
    return "😐 Neutral"

# check if the sentence is question
def is_question(tokens, prompt):
    return prompt.strip().endswith("?") or any(word in tokens for word in question_words)

# it will detect when asking or recommending.
def detect_list_request(tokens):
    return any(word in tokens for word in list_keywords)

# Export useful constants for reuse
def get_emotion_keywords():
    return positive_words | negative_words | question_words | list_keywords
