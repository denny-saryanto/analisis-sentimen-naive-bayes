import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, f1_score, precision_score, classification_report
from sklearn.naive_bayes import MultinomialNB
from text_preprocessing import TextPreprocessing
import pickle
import json
from datetime import datetime

class Vectorize():
    def __init__(self, input):
        self.input = input
        self.tfidf = TfidfVectorizer(use_idf=True, norm='l2', smooth_idf=False)
        self.tfidf.fit(self.input)
    
    def get_transform(self):
        return self.tfidf.transform(self.input).toarray()
    
    def export(self):
        filename = 'app/pretrained/tfidf.pickle'
        pickle.dump(self.tfidf, open(filename, "wb"))
        return 'TFIDF Export Success'

class Model():
    def __init__(self, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.model = MultinomialNB(alpha=1.0 , fit_prior=True, class_prior=None)
        self.model.fit(self.X_train, self.y_train)
    
    def kfold_cross_val_accuracy(self, text, label):
        self.cv = KFold(n_splits=10, random_state=None)
        self.scores = cross_val_score(self.model, text, label, cv=self.cv, scoring='accuracy')
        return self.scores.mean()
    
    def get_reports(self):
        pred = self.model.predict(self.X_test)
        y_test = self.y_test
        return [accuracy_score(y_test, pred), precision_score(y_test, pred, average=None, labels=['positif', 'netral', 'negatif']), f1_score(y_test, pred, average=None, labels=['positif', 'netral', 'negatif']), recall_score(y_test, pred, average=None, labels=['positif', 'netral', 'negatif'])]
        # return classification_report(y_test, pred, target_names=['positif', 'netral', 'negatif'])
    
    def get_confusion_matrix(self):
        pred = self.model.predict(self.X_test)
        y_test = self.y_test
        return confusion_matrix(y_test, pred, labels=['positif', 'netral', 'negatif'])
    
    def export_json(self, data):
        with open('app/info/data.json', 'w') as write_f:
            json.dump(data, write_f)

    def export(self):
        filename_model = 'app/pretrained/model.pickle'
        pickle.dump(self.model, open(filename_model, 'wb'))
        result = self.get_reports()
        cfm = self.get_confusion_matrix()
        export_info = {
            "model_name" : "model.pickle",
            "tfidf_name" : "tfidf.pickle",
            "data_time" : datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 
            "model_reports" : {
                "accuracy_score" : round(result[0], 2),
                "precision_score" : round(result[1].mean(), 2),
                "f1_score" : round(result[2].mean(), 2),
                "recall_score" : round(result[3].mean(), 2),
                "cfm" : cfm.tolist(),
            },
        }
        self.export_json(export_info)
        return 'Export Model Success', self.get_confusion_matrix()