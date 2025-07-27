"""HANGMAN GAME IN PYTHON."""

import random

HANGMAN_ART = r"""
 _                                             
| |                                            
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __  
| '_ \ / _' | '_ \ / _' | '_ ' _ \ / _' | '_ \ 
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                    __/ |                      
                   |___/
"""
WORD_LIST = [  # 369 words
    "about", "above", "according", "account", "across", "action", "active",
    "activity", "address", "after", "again", "against", "agree", "allow",
    "almost", "alone", "along", "already", "always", "among", "amongst",
    "amount", "animal", "another", "anything", "apart", "appear", "apple",
    "apply", "approach", "argue", "around", "available", "avoid", "aware",
    "basic", "battle", "beauty", "become", "before", "begin", "behavior",
    "behind", "believe", "below", "better", "between", "birth", "black",
    "blood", "board", "brain", "break", "bring", "budget", "build",
    "building", "business", "called", "camera", "career", "carry", "cause",
    "center", "central", "century", "certain", "chair", "change", "check",
    "child", "children", "civil", "claim", "class", "clean", "clear", "close",
    "coach", "college", "color", "common", "community", "company", "control",
    "country", "course", "cover", "create", "crime", "cross", "culture",
    "current", "daily", "damage", "dance", "danger", "dealer", "death",
    "debate", "decide", "defeat", "defend", "define", "degree", "demand",
    "depend", "desert", "design", "detail", "develop", "development",
    "device", "differ", "different", "dinner", "direct", "doctor", "dollar",
    "domain", "double", "doubt", "dream", "dress", "drink", "drive", "driver",
    "during", "early", "earth", "economic", "economy", "editor", "education",
    "effect", "effort", "eight", "eleven", "emerge", "empty", "energy",
    "english", "enjoy", "enough", "enter", "environment", "especially",
    "event", "every", "everything", "exact", "example", "exist", "experience",
    "extra", "faith", "false", "family", "father", "fault", "favor", "field",
    "fight", "figure", "final", "finish", "first", "floor", "focus", "follow",
    "following", "force", "found", "freedom", "friend", "front", "fruit",
    "funny", "future", "garden", "general", "glass", "government", "grade",
    "grant", "grass", "great", "green", "group", "growth", "guard", "guess",
    "guest", "guide", "happy", "health", "heart", "heavy", "history", "hotel",
    "house", "however", "human", "ideal", "image", "important", "include",
    "indeed", "individual", "industry", "information", "inside", "interest",
    "international", "issue", "joint", "judge", "knowledge", "large", "later",
    "laugh", "leader", "league", "learn", "leave", "legal", "level", "light",
    "listen", "little", "living", "local", "machine", "major", "management",
    "market", "match", "material", "matter", "media", "meeting", "member",
    "million", "minor", "minute", "model", "moment", "money", "month",
    "morning", "mother", "mouth", "nation", "national", "natural", "nature",
    "necessary", "never", "night", "north", "nothing", "number", "object",
    "occur", "offer", "office", "often", "order", "organization", "outside",
    "owner", "paper", "parent", "particular", "party", "peace", "people",
    "perhaps", "period", "person", "phone", "physical", "picture", "piece",
    "place", "planet", "plant", "player", "point", "policy", "position",
    "possible", "power", "present", "press", "pressure", "problem", "process",
    "produce", "product", "program", "project", "provide", "public",
    "purpose", "quality", "question", "really", "reason", "record",
    "relationship", "remain", "report", "research", "resource", "response",
    "result", "return", "right", "school", "science", "second", "security",
    "sense", "serious", "service", "several", "should", "simple", "small",
    "social", "society", "something", "sound", "south", "special", "specific",
    "start", "state", "still", "story", "street", "strong", "student",
    "study", "subject", "success", "summer", "support", "system", "teacher",
    "technology", "theory", "thing", "think", "three", "today", "together",
    "travel", "under", "understand", "value", "video", "water", "weather",
    "winter", "world", "write", "young"
]
HANGMAN_LIVES_MAP = {
    0: r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
""",

    1: r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
""",

    2: r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
""",

    3: r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
""",

    4: r"""
  +---+
  |   |
  O   |
 /    |
      |
      |
=========
""",

    5: r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========
""",

    6: r"""
  +---+
  |   |
      |
      |
      |
      |
=========
"""
}

def play_hangman():
    """Play Hangman Game."""

    print(HANGMAN_ART)
    keyword = random.choice(WORD_LIST)
    word_len = len(keyword)
    guess_word = "_" * word_len
    keyword_letters = set(keyword)
    lives = 6

    while True:
        print(f"Word to guess: {guess_word}")
        guess_letter = input("Guess a letter: ").strip().lower()

        if len(guess_letter) > 1 and guess_letter in keyword:
            print(guess_word)
        elif guess_letter in keyword_letters:
            guess_word = "".join(
                [guess_letter if keyword[idx] == guess_letter else char \
                 for idx, char in enumerate(guess_word)]
            )
            print(guess_word)
            keyword_letters.remove(guess_letter)
        elif guess_letter in guess_word:
            print("You've already guessed", guess_letter)
        else:
            lives -= 1
            print(f"You guessed {guess_letter}, that's not in the word. "
                  "You lose a life.")

        if len(keyword_letters) == 0:
            print("YOU WIN!")
            break

        print(HANGMAN_LIVES_MAP[lives], end="")
        if lives == 0:
            print(f"IT WAS {keyword}. YOU LOSE.".center(79, "*"))
            break
        print(f"{lives}/6 LIVES LEFT".center(79, "*"))


if __name__ == "__main__":
    play_hangman()
