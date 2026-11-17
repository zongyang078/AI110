"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    # New additions
    "proud",
    "hopeful",
    "fire",      # slang: means really good
    "slaps",     # slang: means awesome
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    # New additions
    "trash",       # slang: means bad
    "exhausted",
    "stuck",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)

# --- New posts added by me ---
SAMPLE_POSTS.append("Oh great, another Monday 🙄")
TRUE_LABELS.append("negative")   # sarcasm: sounds positive but means negative

SAMPLE_POSTS.append("This song is fire 🔥")
TRUE_LABELS.append("positive")   # slang: "fire" = really good

SAMPLE_POSTS.append("I'm exhausted but proud of myself")
TRUE_LABELS.append("mixed")      # negative + positive feelings

SAMPLE_POSTS.append("lol that was lowkey trash")
TRUE_LABELS.append("negative")   # slang: "trash" = bad

SAMPLE_POSTS.append("Just got my results back")
TRUE_LABELS.append("neutral")    # factual, no emotion

SAMPLE_POSTS.append("I love getting stuck in traffic")
TRUE_LABELS.append("negative")   # sarcasm: nobody loves traffic

SAMPLE_POSTS.append("ngl this class slaps 💯")
TRUE_LABELS.append("positive")   # slang: "slaps" = awesome

SAMPLE_POSTS.append("Whatever, it is what it is")
TRUE_LABELS.append("neutral")    # resigned, no strong emotion