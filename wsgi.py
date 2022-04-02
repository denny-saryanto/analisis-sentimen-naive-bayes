from main import app
import nltk
 
if __name__ == "__main__":
        nltk.download('punkt')
        nltk.download('stopwords')
        app.run()