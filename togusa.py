#!./env/bin/python

import logging

import flask
import langid
import textblob
import textblob_de

DEBUG=True

app = flask.Flask(__name__)
app.config.from_object(__name__)

helpscreen="""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset=utf-8>
        <title>Togusa Textanalysis Api</title>
        <style>
        </style>
    </head>
    <body>
        <h1>Togusa Textanalysis Api</h1>

        <h2>/api/language - Language detection</h2>
        <pre><code>
$ curl -H "Content-Type: application/json" -X POST \\
  -d '{"text": "The Aneristic Principle is that of apparent order; the Eristic Principle is that of apparent disorder."}' \\
  127.0.0.1:5000/api/language
{
  "lang": "en",
  "probabilities": [
    "en",
    1.0
  ],
  "text": "The Aneristic Principle is that of apparent order; the Eristic Principle is that of apparent disorder."
}
        </code></pre>

        <h2>/api/keywords - Keyword extraction</h2>
        <pre><code>
$ curl -H Content-Type: application/json -X POST \\
  -d '{"text": "The Aneristic Principle is that of apparent order; the Eristic Principle is that of apparent disorder."}' \\
  127.0.0.1:5000/api/keywords
{
  "keywords": [
    "aneristic principle",
    "apparent order",
    "eristic principle",
    "apparent disorder"
  ],
  "lang": "en",
  "text": "The Aneristic Principle is that of apparent order; the Eristic Principle is that of apparent disorder."
}
        </code></pre>
    </body>
</html>
"""

@app.route("/")
def help():
    return helpscreen

@app.route('/api/language', methods=['POST'])
def detect_language():
    text = flask.request.json['text']
    languages = langid.classify(text)
    return flask.jsonify({
        'lang': languages[0],
        'probabilities': languages,
        'text': text,
    })   

@app.route('/api/keywords', methods=['POST'])
def extract_keywords():
    text = flask.request.json['text']
    language = langid.classify(text)[0]
    if language == 'de':
        article_nlp = textblob_de.TextBlobDE(text).strip().strip('\n').strip('\\n').strip('\t')
    else:
        article_nlp = textblob.TextBlob(text).strip().strip('\n').strip('\\n').strip('\t')
    return flask.jsonify({
        'keywords': article_nlp.noun_phrases,
        'lang': language,
        'text': text,
    })

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%s')
    app.run()
