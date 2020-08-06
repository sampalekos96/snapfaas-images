import json
import nltk
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

nltk.data.path = ['/srv/package/nltk_data']

def handle(request):
    if 'bayes' in request:
        analyse = TextBlob(request['analyse'], analyzer=NaiveBayesAnalyzer())
    else:
        analyse = TextBlob(request['analyse'])

    num_sentences = len(analyse.sentences)

    results = []
    for sentence in analyse.sentences:
        if 'bayes' in request:
            result = (sentence.sentiment.classification, sentence.sentiment.p_pos, sentence.sentiment.p_neg)
        else:
            result = (sentence.sentiment.subjectivity, sentence.sentiment.polarity)
        results.append(result)

    retVal = {"results": results, "num_sentences": num_sentences}

    return retVal
