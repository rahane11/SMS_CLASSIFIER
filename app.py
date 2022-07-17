from flask import Flask, render_template, request
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from string import punctuation

app = Flask(__name__)

vector= pickle.load(open('artifacts/Vectorizer.pkl', 'rb'))
model = pickle.load(open('artifacts/model.pkl', 'rb'))


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/predict', methods =["POST", "GET"])
def predict():
    text = str(request.form.get("text"))
    text1 = transofrm_text(text)
    vector_ip = vector.transform([text1])
    result = model.predict(vector_ip)[0]
    if result == 1:
        return "SMS is SPAM"
    else:
        return "SMS is not SPAM"

    

def transofrm_text(text):
    """
    take an sms string and convert to a list of stemmed words
    """
    ps = WordNetLemmatizer()
    text = text.lower()
    text = re.sub(r'<[^<>]+>' , ' ' , text)
    text = re.sub(r'[0-9]+' , 'number' , text)
    text = re.sub(r'(http|https)://[^\s]*' , 'https' , text)
    text = re.sub(r'[^\s]+@[^\s]+' , 'email' , text)
    text = re.sub(r'[$]+' , 'dollar' , text)
    text = nltk.word_tokenize(text)
    text = [i for i in text if i.isalnum()]
    text = [i for i in text if i not in stopwords.words("english") and i not in punctuation]
    text = [ps.lemmatize(i) for i in text]
    return " ".join(text)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port = 5000)