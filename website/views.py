from flask import Blueprint, render_template, request, jsonify
views = Blueprint('views', __name__)

from googletrans import Translator
translator = Translator()

@views.route('/', methods=['GET', 'POST'])
@views.route('/index', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.json
        text = data['userMessage']
        lang = data['lang']
        translatedText = translator.translate(text, dest=lang)
        
        return jsonify({"translatedMessage": translatedText.text})
    return render_template("index.html")
