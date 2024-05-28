from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from heapq import nlargest

def extract_summary(text, num_sentences=8):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(sentences)

    # Get feature names (words) from the vectorizer
    feature_names = vectorizer.get_feature_names_out()

    # Calculate TF-IDF scores for each sentence
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        tfidf_sentence = matrix[i].toarray()[0]
        for j, score in enumerate(tfidf_sentence):
            if score > 0:
                word = feature_names[j]
                if word in sentence:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = score
                    else:
                        sentence_scores[sentence] += score

    # Select top N sentences based on scores
    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    
    return summary
