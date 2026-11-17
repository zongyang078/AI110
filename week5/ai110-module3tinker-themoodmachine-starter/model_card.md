# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

## 1. Model Overview

**Model type:**  
I compared both models: the rule based model and the ML model (Naive Bayes).

**Intended purpose:**  
Classify short social media posts or messages into mood labels: positive, negative, neutral, or mixed.

**How it works (brief):**  
The rule based version preprocesses text (lowercase, remove punctuation), then scores each token (+1 for positive words, -1 for negative words) with negation handling (e.g., "not happy" flips from +1 to -1). The score maps to a label: >0 = positive, <0 = negative, 0 = neutral.  
The ML version uses a Naive Bayes classifier trained on bag-of-words features extracted from the labeled dataset.

## 2. Data

**Dataset description:**  
14 labeled posts total: 6 from the starter repo + 8 added by me. Posts range from clearly positive/negative to sarcastic, slang-heavy, and emotionally mixed.

**Labeling process:**  
Labels were assigned by me based on what I thought each post "really meant." Some were tricky — for example, "This is fine" could be neutral or passive-aggressive depending on context. I labeled it neutral. "I'm fine 🙂" in real life often means the opposite of fine, but without more context I'd lean neutral/positive.

**Important characteristics of your dataset:**  
- Contains slang: "fire", "slaps", "trash", "lowkey", "ngl"
- Contains emojis: 🙄, 🔥, 💯
- Includes sarcasm: "Oh great, another Monday", "I love getting stuck in traffic"
- Some posts express mixed feelings: "exhausted but proud", "tired but hopeful"
- Contains short ambiguous messages: "This is fine", "Just got my results back"

**Possible issues with the dataset:**  
- Very small (only 14 examples) — not enough to generalize
- Imbalanced: more negative/positive examples than mixed/neutral
- All in casual English — no other languages or dialects
- Labels are subjective — another person might label some posts differently

## 3. How the Rule Based Model Works

**Your scoring rules:**  
- Preprocess: lowercase, remove punctuation (keep apostrophes for contractions), split into tokens
- Scoring: +1 for each positive word, -1 for each negative word
- Negation handling: if a negation word (not, don't, can't, never, won't, isn't, etc.) appears before a sentiment word, the polarity flips. Example: "not happy" → -1 instead of +1
- Thresholds: score > 0 → positive, score < 0 → negative, score == 0 → neutral
- Vocabulary: 14 positive words (including slang: fire, slaps) and 13 negative words (including slang: trash)

**Strengths of this approach:**  
- Fully transparent: you can trace exactly why each prediction was made
- Works well on simple, direct sentences: "I love this class so much" → positive
- Negation handling correctly flips "not happy" and "not bad"

**Weaknesses of this approach:**  
- Cannot detect sarcasm: "Oh great, another Monday 🙄" is predicted positive because "great" is in the word list
- Cannot detect mixed emotions: "exhausted but proud" scores to 0 (neutral) instead of mixed
- Emojis are stripped and ignored — 🙄 and 🔥 carry no weight
- Idioms like "can't stand" are not handled as a unit
- Any word not in the vocabulary is invisible to the model

## 4. How the ML Model Works

**Features used:**  
Bag of words using CountVectorizer — each word becomes a feature, and its count becomes the value.

**Training data:**  
The model trained on all 14 posts in SAMPLE_POSTS with labels from TRUE_LABELS.

**Training behavior:**  
With only 14 examples, the model memorized the training data perfectly and achieved 100% accuracy. This is overfitting — it learned the specific answers, not generalizable patterns.

**Strengths and weaknesses:**  
Strengths: handled sarcasm, mixed emotions, and slang correctly on training data because it memorized those exact examples.  
Weaknesses: 100% accuracy is misleading — with so few examples, it cannot generalize to unseen text. It is also a black box: hard to explain why it made a specific prediction.

## 5. Evaluation

**How you evaluated the model:**  
Both models were evaluated on the same 14 labeled posts in dataset.py.  
- Rule based accuracy: 71% (10/14 correct)
- ML accuracy: 100% (14/14 correct, but overfitting)

**Examples of correct predictions:**  
- "I love this class so much" → positive (rule based matched "love" → +1)
- "I am not happy about this" → negative (negation flipped "happy" from +1 to -1)
- "lol that was lowkey trash" → negative (matched "trash" → -1)

**Examples of incorrect predictions (rule based):**  
- "Oh great, another Monday 🙄" → predicted positive, true negative. "great" matched +1 but the sentence is sarcastic.
- "I love getting stuck in traffic" → predicted neutral, true negative. love(+1) + stuck(-1) = 0, but nobody actually loves traffic. Sarcasm.
- "I'm exhausted but proud of myself" → predicted neutral, true mixed. exhausted(-1) + proud(+1) = 0, but both emotions are genuinely present.

## 6. Limitations

- **Small dataset**: 14 examples is far too few for any model to learn robust patterns
- **Sarcasm is undetectable** by keyword counting — "Oh great" will always look positive
- **Mixed emotions collapse to neutral** because positive and negative scores cancel out to 0
- **Emojis are ignored** during preprocessing
- **Idioms** like "can't stand" are not handled as multi-word units
- **English-only** and biased toward American internet slang
- **ML model overfits** — 100% accuracy on training data means nothing about real-world performance

## 7. Ethical Considerations

- **Misclassifying distress**: if someone writes "I'm fine 🙂" while struggling, the model might miss it. In a mental health context this could be dangerous.
- **Cultural/dialect bias**: the vocabulary is optimized for American English internet slang. Posts in AAVE, British English, or other dialects might be misclassified.
- **Privacy**: analyzing personal messages for mood raises consent and privacy concerns.
- **Sarcasm misreads**: flagging a sarcastic complaint as "positive" could lead to ignoring valid frustration.

## 8. Ideas for Improvement

- Add more labeled data (at least 100+ examples) for better ML generalization
- Use TF-IDF instead of CountVectorizer to weight rare words higher
- Add emoji-to-sentiment mapping (🙄 → negative, 🔥 → positive)
- Handle multi-word expressions like "can't stand" as single units
- Add a "mixed" detection rule: if both positive and negative words are present, return mixed instead of neutral
- Use a proper train/test split instead of evaluating on training data
- Try a pre-trained transformer model (like BERT) for better contextual understanding