import webbrowser
from sklearn.externals import joblib
from flask import Flask, render_template, request


app = Flask(__name__)

def detection(model, x):
    x = str(x)
    language = model.predict([x])[0]
    proba = model.predict_proba([x])
    print(proba)
    if len(x) <= 25:
        language = 'frase demasiado corta (<25 chars.)'
    elif language == 'fr':
        language = 'francés'
    elif language == 'pt':
        language = 'portugués'
    elif language == 'it':
        language = 'italiano'
    elif language == 'en':
        language = 'inglés'
    elif language == 'es':
        language = 'español'
    return language

@app.route('/')
def student():
    return render_template('index.html', result={'language': None})

@app.route('/result', methods=['POST', 'GET'])
def result():
    result = request.form
    if request.method == 'POST':
        dict_result = dict(result)
        text = dict_result['text_to_language']
        lang = detection(model, text)
    else:
        lang = None
    return render_template('index.html', result={'language': lang.upper()})


if __name__ == '__main__':
    model = joblib.load('models/model.pkl')
    url = "http://localhost:5000"
    webbrowser.open_new(url)
    app.run()