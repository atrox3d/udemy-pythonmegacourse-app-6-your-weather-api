from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('translator-home.html')


@app.route('/api/v1/<word>')
def translation(word):
    return {
        "word": word,
        "definition": str.upper(word)
    }


if __name__ == '__main__':
    app.run(debug=True, port=5001)
