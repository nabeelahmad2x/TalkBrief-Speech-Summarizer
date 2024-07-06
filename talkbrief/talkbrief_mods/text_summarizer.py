from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize, word_tokenize
from heapq import nlargest

def count_words(text):
    """Count the total number of words in the text."""
    return len(word_tokenize(text))

def calculate_num_sentences(text, summary_length):
    """Calculate the number of sentences needed for the summary."""
    total_words = count_words(text)
    target_word_count = (total_words * int(summary_length)) / 100
    average_sentence_length = total_words / len(sent_tokenize(text))
    num_sentences = round(target_word_count / average_sentence_length)
    return max(1, num_sentences)

def extract_summary(text, summary_length):
    num_sentences = calculate_num_sentences(text, summary_length)
    sentences = sent_tokenize(text)

    vectorizer = TfidfVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(sentences)

    feature_names = vectorizer.get_feature_names_out()

    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        tfidf_sentence = matrix[i].toarray()[0]
        for j, score in enumerate(tfidf_sentence):
            if score > 0:
                word = feature_names[j]
                # Check if the word is in the sentence using word boundaries
                if f" {word} " in f" {sentence} ":
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = score
                    else:
                        sentence_scores[sentence] += score

    summary_sentences = nlargest(int(num_sentences), sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    
    return summary
