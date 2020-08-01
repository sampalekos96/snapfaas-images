This sentiment analysis function uses the [Python TextBlob library](https://textblob.readthedocs.io) to give a sentiment analysis of the provided text.

Function request should be like:

{'bayes': null, 'analyse': paragraph to be analyzed}

or

{'analyse': paragraph to be analyzed}

The existences of 'bayes' tells the function to use NativeBayesAnalyzer a built-in of TextBlob.

Function response is like:

{'results': list of results for each sentence, 'num_sentences': number of sentences}
