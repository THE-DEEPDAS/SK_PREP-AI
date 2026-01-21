import re

def extract_keywords(model_answer):

    words = re.findall(r'\b[A-Za-z]{5,}\b', model_answer)
    keywords = list(set(words))

    return keywords[:15]


def keyword_score(user_answer, keywords):

    matched = 0

    for k in keywords:
        if k.lower() in user_answer.lower():
            matched += 1

    percent = (matched / len(keywords)) * 100

    return percent
