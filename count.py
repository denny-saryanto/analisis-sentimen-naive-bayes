import pandas as pd
import string
from nltk.tokenize import word_tokenize

class CountDF():
    def __init__(self, df):
        if isinstance(df, pd.DataFrame):
            self.df = df
        else:
            self.df = pd.read_csv(df)
    
    def count_labels(self, labels):
        self.result = self.df[labels].value_counts()
        return self.result
    
    def _clean(self, labels):
        arr = []
        for word in self.df[labels]:
            word = word.translate(str.maketrans('','',string.punctuation)).lower()
            arr.append(word)
        return arr
    
    def _tokenize_list(self, labels):
        arr = []
        for word in self._clean(labels):
            arr.append(word_tokenize(word))
        return arr
    
    def count_words(self, labels, words=10):
        text_tokenize = self._tokenize_list(labels)
        bow, dict_words = {}, {}
        bow_sort = None
        for text in text_tokenize:
            for token in text:
                if token not in bow.keys():
                    bow[token] = 1
                else:
                    bow[token] += 1
        if words == 'all':
            bow_sort = sorted(bow.items(), key=lambda x: x[1], reverse=True)
        else:
            bow_sort = sorted(bow.items(), key=lambda x: x[1], reverse=True)[:words]
        for data in bow_sort:
            dict_words[data[0]] = data[1]
        return dict_words
    
    def count_words_label(self, texts, words=10):
        texts = texts.dropna()
        texts = texts.reset_index(drop=True)
        texts = texts.apply(word_tokenize)
        bow, dict_words = {}, {}
        bow_sort = None
        for text in texts:
            for token in text:
                if token not in bow.keys():
                    bow[token] = 1
                else:
                    bow[token] += 1
        if words == 'all':
            bow_sort = sorted(bow.items(), key=lambda x: x[1], reverse=True)
        else:
            bow_sort = sorted(bow.items(), key=lambda x: x[1], reverse=True)[:words]
        for data in bow_sort:
            dict_words[data[0]] = data[1]
        return dict_words
    
    def length_df(self):
        return len(self.df)