import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


def summarize(text, per):
    nlp = spacy.load('en_core_web_sm') 
    doc= nlp(text)
    tokens= [token.text for token in doc]           ### Word Tokenizer
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):       ### Check if the token is a Stopword or not.
            if word.text.lower() not in punctuation:            ### Select those tokens that are not punctuations. 
                if word.text not in word_frequencies.keys():        ### This loop is for scoring each tokens
                    word_frequencies[word.text] = 1              
                else:
                    word_frequencies[word.text] += 1

    #### NORMALIZE the scores by dividing by the maximum score.
    max_frequency = max(word_frequencies.values())        
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    
    sentence_tokens= [sent for sent in doc.sents]           #### Sentence tokenizer
    sentence_scores = {}
    
    for sent in sentence_tokens:            
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    """
        In the above loop, for each sentences we will take the words ans then we will check if this 
        word in the lower form is present in the word_frequencie dictionary. If it is there then the 
        sentence is added to the sentence_scores dictionary with the score of the word.

    """
    
    select_length = int(len(sentence_tokens)*per)     ### Percentage of sentences that are needed.
    summary = nlargest(select_length, sentence_scores,key= sentence_scores.get) ### Obtain the top n sentences.
    final_summary = [sentence.text for sentence in summary]
    summary = ''.join(final_summary)
    return summary
    




"""
    REFERENCE:
    1. https://www.activestate.com/blog/how-to-do-text-summarization-with-python/
    2. Download --> python -m spacy download en_core_web_sm
"""