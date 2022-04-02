from flask import Flask, render_template, request, Response, make_response, jsonify, redirect, url_for, send_file
import pickle, os, glob, json
from count import CountDF
from text_preprocessing import TextPreprocessing
from model import Vectorize, Model
import pandas as pd
from shutil import copyfile
from sklearn.model_selection import train_test_split
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from whitenoise import WhiteNoise

#-- Declare Input --#
df = 'dataset/dataframe/df.csv'

PATH= {
    'NORMALFILE' : 'dataset/preprocessing/normalisasi.csv',
    'STOPWORDS' : 'dataset/preprocessing/stopwords_id.txt',
    'KAMUS_EMOJI' : 'dataset/preprocessing/emoji.csv',
    'KAMUS_EMOTICON' : 'dataset/preprocessing/emoticon.json',
}
#-- Declare Input End --#

#-- Web Based Start --#
app = Flask(__name__)

app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")

@app.route('/', methods=['POST', 'GET'])
def main():
    return redirect('/dashboard', 302)

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    return render_template("dashboard.html")

@app.route('/model', methods=['POST', 'GET'])
def model_manager():
    return render_template('model.html')

@app.route('/api/predict', methods=['POST', 'GET'])
def predict_input():
    PATH_FILE = 'pretrained/'
    if request.method == 'POST':
        data = request.get_json()
        filename_model = PATH_FILE + data['model_name']
        filename_tfidf = PATH_FILE + data['tfidf_name']
        tfidf = pickle.load(open(filename_tfidf, 'rb'))
        model = pickle.load(open(filename_model, 'rb'))
        if data['type'] == 'text':
            text_dataframe = pd.DataFrame()
            text_dataframe['text'] = [data['input_text']]
            text_preprocess = TextPreprocessing(text_dataframe['text'], None, PATH)
            result = text_preprocess.output(export=False)
            features_req_input = tfidf.transform(result['text_string_stemmed']).toarray()
            pred = model.predict(features_req_input)
            return jsonify({'result' : pred.tolist()})
        else:
            return jsonify({'result' : 'error'})

@app.route('/api/predict/file', methods=['POST'])
def predict_input_file():
    PATH_FILE = 'pretrained/'
    if request.method == 'POST':
        data = request.files['file']
        data = pd.read_csv(data)
        filename_model_file = PATH_FILE + 'model.pickle'
        filename_tfidf_file = PATH_FILE + 'tfidf.pickle'
        model = pickle.load(open(filename_model_file, 'rb'))
        tfidf = pickle.load(open(filename_tfidf_file, 'rb'))
        text_preprocess = TextPreprocessing(data['text'], None, PATH)
        result = text_preprocess.output(export=False)
        features = tfidf.transform(result['text_string_stemmed']).toarray()
        data['sentiment'] = model.predict(features)
        data.to_csv('dataset/predict_file/pred.csv', index=False)
        count = CountDF('dataset/predict_file/pred.csv')
        count_result = count.count_labels(labels='sentiment')
        count_json = {
            'result' : "Upload Success",
            'index' : count_result.index.values.tolist(),
            'values' : count_result.values.tolist(),
            'length_df' : count.length_df(),
        }
        return jsonify(count_json)
    else:
        return jsonify({"result" : "error"})

@app.route('/api/predict/file/download', methods=['GET'])
def predict_download_file():
    if request.method == 'GET':
        return send_file('dataset/predict_file/pred.csv', mimetype='text/csv', attachment_filename='pred.csv', as_attachment=True)

@app.route('/api/file/stopwords', methods=['GET', 'POST'])
def file_stopwords_replace():
    if request.method == 'GET':
        return send_file('dataset/preprocessing/stopwords_id.txt', mimetype='text/*', attachment_filename='stopwords_id.txt', as_attachment=True)
    elif request.method == 'POST':
        data = request.files['file']
        if data != '' or data != None:
            data.filename = 'stopwords_id.txt'
            data.save('dataset/preprocessing/'+data.filename)
            PATH['STOPWORDS'] = 'dataset/preprocessing/stopwords_id.txt'
            return jsonify({'result' : 'replace stopwords success'})
        else:
            return jsonify({'result' : 'cant replace stopwords'})
    else:
        return jsonify({'result' : 'error request'})

@app.route('/api/file/emoji', methods=['GET', 'POST'])
def file_emoji_replace():
    if request.method == 'GET':
        return send_file('dataset/preprocessing/emoji.csv', mimetype='text/csv', attachment_filename='emoji.csv', as_attachment=True)
    elif request.method == 'POST':
        data = request.files['file']
        if data != '' or data != None:
            data.filename = 'emoji.csv'
            data.save('dataset/preprocessing/'+data.filename)
            PATH['KAMUS_EMOJI'] = 'dataset/preprocessing/emoji.csv'
            return jsonify({'result' : 'replace emoji success'})
        else:
            return jsonify({'result' : 'cant replace emoji'})
    else:
        return jsonify({'result' : 'error request'})

@app.route('/api/file/emoticon', methods=['GET', 'POST'])
def file_emoticon_replace():
    if request.method == 'GET':
        return send_file('dataset/preprocessing/emoticon.json', mimetype='application/json', attachment_filename='emoticon.json', as_attachment=True)
    elif request.method == 'POST':
        data = request.files['file']
        if data != '' or data != None:
            data.filename = 'emoticon.json'
            data.save('dataset/preprocessing/'+data.filename)
            PATH['KAMUS_EMOTICON'] = 'dataset/preprocessing/emot.json'
            return jsonify({'result' : 'replace emoticon success'})
        else:
            return jsonify({'result' : 'cant replace emoticon'})
    else:
        return jsonify({'result' : 'error request'})

@app.route('/api/file/normalization', methods=['GET', 'POST'])
def file_normalization_replace():
    if request.method == 'GET':
        return send_file('dataset/preprocessing/normalisasi.csv', mimetype='text/csv', attachment_filename='normalisasi.csv', as_attachment=True)
    elif request.method == 'POST':
        data = request.files['file']
        if data != '' or data != None:
            data.filename = 'normalisasi.csv'
            data.save('dataset/preprocessing/'+data.filename)
            PATH['NORMALFILE'] = 'dataset/preprocessing/normalisasi.csv'
            return jsonify({'result' : 'replace stopwords success'})
        else:
            return jsonify({'result' : 'cant replace stopwords'})
    else:
        return jsonify({'result' : 'error request'})

@app.route('/api/count/labels', methods=['POST'])
def api_counts_labels():
    if request.method == 'POST':
        count = CountDF(df)
        count_result = count.count_labels(labels='sentiment')
        count_json = {
            'index' : count_result.index.values.tolist(),
            'values' : count_result.values.tolist(),
            'length_df' : count.length_df(),
        }
        return jsonify(count_json)
    else:
        return jsonify({'result' : 'error'})

@app.route('/api/count/words', methods=['POST'])
def api_counts_words():
    if request.method == 'POST':
        df = pd.read_csv('dataset/preprocessing/df_preprocess.csv')
        count = CountDF('dataset/preprocessing/df_preprocess.csv')
        count_result = count.count_words(labels='stopwords_stemmed', words=10)
        count_result_positive = count.count_words_label(df['text_string_stemmed'].loc[df['label'] == 'positif'], words=10)
        count_result_neutral = count.count_words_label(df['text_string_stemmed'].loc[df['label'] == 'netral'], words=10)
        count_result_negative = count.count_words_label(df['text_string_stemmed'].loc[df['label'] == 'negatif'], words=10)
        count_json = {
            'index' : list(count_result.keys()),
            'values' : list(count_result.values()),
            'length_df' : count.length_df(),
            'positive_words' : {
                'label' : list(count_result_positive.keys()),
                'value' : list(count_result_positive.values()),
            },
            'neutral_words' : {
                'label' : list(count_result_neutral.keys()),
                'value' : list(count_result_neutral.values()),
            },
            'negative_words' : {
                'label' : list(count_result_negative.keys()),
                'value' : list(count_result_negative.values()),
            }
        }
        return jsonify(count_json)
    else:
        return jsonify({'result' : 'error'})

@app.route('/api/info', methods=['GET'])
def api_get_info():
    if request.method == 'GET':
        arr_stop = []
        count = CountDF(df)
        #Get All Words
        get_all_words = count.count_words(labels='text', words='all')
        # Get All Stopwords
        txt_stopword = pd.read_csv(PATH['STOPWORDS'], names=['stopwords_id'], header=None)
        arr_stop.append(txt_stopword['stopwords_id'][0].split(' '))
        # Get Normalization Data
        load_word = pd.read_csv(PATH['NORMALFILE'])
        return jsonify({
            'all_words' : len(get_all_words.keys()),
            'total_stopwords' : len(arr_stop[0]),
            'total_normalization' : len(load_word),
        })

@app.route('/api/file/', methods=['GET'])
def api_file_manager_get():
    get_size = []
    folder_file = 'pretrained'
    for file_data in os.listdir(folder_file):
        file_stat = os.stat(folder_file + file_data)
        size = file_stat.st_size / (1024 * 1024)
        get_size.append(round(size, 2))
    return jsonify({
        'list_files' : os.listdir(folder_file),
        'list_files_size' : get_size,
        'total_size_file' : sum(get_size),
        'total_file' : len(os.listdir(folder_file)),
    })

@app.route('/api/file/merge', methods=['POST', 'GET'])
def api_file_merge():
    if request.method == 'POST' and 'file' in request.files:
        file_upload = request.files['file']
        if file_upload != '' or file_upload != None:
            file_upload.save(os.path.join('dataset/dataframe', file_upload.filename))
            if len(glob.glob('dataset/dataframe/*.csv')) != 0:
                all_filenames = [i for i in glob.glob('dataset/dataframe/*.csv')]
                combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
                combined_csv.to_csv("dataset/dataframe/df.csv", index=False, encoding='utf-8-sig')
                return jsonify({'result' : 'upload and merge success'})
            else:
                return jsonify({'result' : 'no file'})
        else:
            return jsonify({'status' : 'error'})
    elif request.method == 'POST' and 'file' not in request.files:
        data = request.get_json()
        if data['command'] == 'reset':
            for file_name in glob.glob('dataset/dataframe/*.csv'):
                os.remove(file_name)
            copyfile('dataset/dataframe/backup/df.csv', 'dataset/dataframe/df.csv')
            return jsonify({'result' : 'reset success'})
        else:
            return jsonify({'result' : 'fail to reset or split'})
    else:
        return jsonify({'result' : 'error'})

@app.route('/api/model/info', methods=['GET'])
def api_model_info():
    file_json = open('info/data.json', 'r')
    data = json.load(file_json)
    file_json.close()
    return data

@app.route('/api/model/train', methods=['POST'])
def api_model_train():
    if request.method == 'POST':
        start_time = time.time()
        df_csv = pd.read_csv('dataset/dataframe/df.csv')
        full_text_pre = TextPreprocessing(df_csv['text'], df_csv['sentiment'], PATH)
        result = full_text_pre.output(export=True)
        tfidf_train = Vectorize(result['text_string_stemmed'])
        tfidf_train.export()
        text_feature = tfidf_train.get_transform()
        text_feature_label = result['label']
        X_train, X_test, y_train, y_test = train_test_split(text_feature, text_feature_label, random_state=1, test_size=0.2)
        model = Model(X_train, X_test, y_train, y_test)
        model.export()
        time_result = round((time.time() - start_time)/60,2)
        return jsonify({
            'status' : 'Export Model and TFIDF Success',
            'training_time' : time_result,
        })
    else:
        return jsonify({'status' : 'error request'})

if __name__ == '__main__':
    app.run(debug=True, port=33507)
#-- Web Based End --#
