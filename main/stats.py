import re


def get_grams(corpus, n_grams=1):
    """
    generates n_grams given a corpus of text
    Corpus should be a list of documents
    """
    stop = ['', ' ', 'and', 'the', 'to', 'a', 'of', 'for', 'as', 'i', 'with', 'it', 'is', 'on', 'that', 'this', 'can', 'in', 'be', 'has', 'if', 'e', 'o', 'de', 'da', 'do', 'para', 'como', 'eu', 'com', 'isso', 'aquilo', 'é', 'são', 'em', 'sobre', 'pode', 'ser', 'seja', 'tem', 'tenha', 'se', 'faça', 'que', 'um', 'uma', 'na', 'no', 'os', 'as']
    corpus_n = [[re.sub('\W+', '', c).lower() for c in a.split(' ') if re.sub('\W+', '', c).lower() not in stop] for a in corpus]
    if n_grams > 1:
        corpus_n = [[' '.join([b[i + k] for k in range(n_grams)]) for i, a in enumerate(b) if i < len(b) - n_grams + 1] for b in corpus_n]
    return [item for sublist in corpus_n for item in sublist]
