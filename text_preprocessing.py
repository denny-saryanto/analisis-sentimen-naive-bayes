import nltk
import string
import re
import glob
import pandas as pd
import emoji
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nlp_id.lemmatizer import Lemmatizer
import json
from sklearn.model_selection import train_test_split

factory = StemmerFactory()
stemmer = factory.create_stemmer()

class TextPreprocessing():
    def __init__(self, text, label, config):
        self.path = config
        self.text = text
        self.label = label
    
    def translate_emoticon(self, text):
        load_emoji = None
        with open(self.path['KAMUS_EMOTICON']) as f:
            load_emoji = json.load(f)
        for index, keys in enumerate(load_emoji.keys()):
            text = text.replace(keys, load_emoji[keys])
        return text
    
    def convert_emoji(self, text):
        text = re.sub('@[^\s]+','', text)
        text = re.sub('#[^\s]+','', text)
        text = emoji.demojize(text)
        text = text.replace(':', ' ')
        text = ' '.join(text.split())
        return text
    
    def translate_emoji(self, text):
        df_emoji = pd.read_csv(self.path['KAMUS_EMOJI'])
        for index, row in df_emoji.iterrows():
            text = text.replace(row[1].replace(' ', '_'), row[5])
        return text
    
    def clean(self, text):
        text = text.lower().strip() #Ubah Ke Lowercase
        text = re.sub('@[^\s]+','',text) #Menghapus Username
        text = ' '.join(re.sub("(rt )"," ", text).split()) #Menghapus kata 'rt'
        text = re.sub('((www\S+)|(http\S+))', ' ', text) #Menghapus URL
        text = re.sub(r'\d+', ' ', text) #Menghapus Angka
        text = text.encode('ascii', 'replace').decode('ascii') #remove non ASCII (emoticon, chinese word, .etc)
        text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"") #remove tab, new line, ans back slice
        text = text.translate(str.maketrans('','',string.punctuation)).lower() #Menghapus Punctuation
        return text
    
    def tokenize(self, text):
        return word_tokenize(text)
    
    def load_dataset_normalization(self):
        load_word = pd.read_csv(self.path['NORMALFILE'])
        normal_word_dict = {}
        for index, row in load_word.iterrows():
            if row[0] not in normal_word_dict:
                normal_word_dict[row[0]] = row[1]
        return normal_word_dict
    
    def normalisasi(self, data):
        word_dict = self.load_dataset_normalization()
        return [word_dict[term] if term in word_dict else term for term in data]
    
    def stemming(self, data):
        lengthData = len(data)
        base = [[] for i in range(0, lengthData)]
        count = 0
        for list_text in data:
            for text in list_text:
                base[count].append(stemmer.stem(text))
            count = count + 1
        return base
    
    def remove_stopwords(self, data):
        totalIndex = len(data)
        base = [[] for i in range(totalIndex)]
        count = 0
        txt_stopword = pd.read_csv(self.path['STOPWORDS'], names=['stopwords_id'], header=None)
        stopwordTexts = stopwords.words('indonesian')
        stopwordTexts.extend(["yg", "dg", "rt", "dgn", "ny", "d", 'klo', 'kalo', 'amp', 'biar', 'bikin', 'bilang', 'gak', 'ga', 'krn', 'nya', 'nih', 'sih', 'si', 'tau', 'tdk', 'tuh', 'utk', 'ya', 'jd', 'jgn', 'sdh', 'aja', 'n', 't', 'nyg', 'hehe', 'pen', 'u', 'nan', 'loh', 'rt','&amp', 'yah', 'wkwkwkkwwk', 'wkwkwkwkwk', 'wkwkwk','wkkwkw', 'anjirrr'])
        stopwordTexts.extend(txt_stopword["stopwords_id"][0].split(' '))
        stopwordTexts = set(stopwordTexts)
        for x in data:
            for text in x:
                if text not in stopwordTexts:
                    base[count].append(text)
            count = count + 1
        return base
    
    def output(self, export):
        self.dataframe = pd.DataFrame()
        self.dataframe['emoticon'] = self.text.apply(self.translate_emoticon)
        self.dataframe['convert_emoji'] = self.dataframe['emoticon'].apply(self.convert_emoji)
        self.dataframe['translate_emoji'] = self.dataframe['convert_emoji'].apply(self.translate_emoji)
        self.dataframe['cleaned'] = self.dataframe['translate_emoji'].apply(self.clean)
        self.dataframe['tokenize'] = self.dataframe['cleaned'].apply(self.tokenize)
        self.dataframe['normalization'] = self.dataframe['tokenize'].apply(self.normalisasi)
        self.dataframe['stemmed'] = self.stemming(self.dataframe['normalization'])
        self.dataframe['stopwords_stemmed'] = self.remove_stopwords(self.dataframe['stemmed'])
        self.dataframe['text_string_stemmed'] = self.dataframe['stopwords_stemmed'].apply(lambda x: ' '.join(x))
        if export == True:
            self.dataframe['label'] = self.label
            self.dataframe = self.dataframe.dropna()
            self.dataframe = self.dataframe.reset_index(drop=True)
            self.dataframe.to_csv('app/dataset/preprocessing/df_preprocess.csv', index=False)
            return self.dataframe
        elif export == False:
            self.dataframe = self.dataframe.dropna()
            self.dataframe = self.dataframe.reset_index(drop=True)
            return self.dataframe
        else:
            print('Error')