from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_most_frequent_response
import os
app = Flask(__name__)

#trainer.train("chatterbot.corpus.english")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("Majestic Admin.html")

@app.route("/chatsetup")
def chatsetup():
    custname = request.args.get('custname')
	#Initialize the DB
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print("removed db.sqlite3")
        english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
    #print(custname)
    #print(os.getcwd())
    trainer = ChatterBotCorpusTrainer(english_bot)
    if os.path.exists(custname + '.yml'):
        print ("found custname yaml file")
        trainer.train(custname)
        #trainer.train("chatterbot.corpus.english")
    else:
        print("file not found")
        trainer.train("abc")
        #trainer.train("chatterbot.corpus.english")
    return "OK" 

@app.route("/chatbox")
def chatbox():
    return render_template("chat.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter",
    preprocessors=['chatterbot.preprocessors.clean_whitespace','chatterbot.preprocessors.unescape_html','chatterbot.preprocessors.convert_to_ascii'],
    silence_performance_warning=True,response_selection_method=get_most_frequent_response,read_only = True,
    logic_adapters=[{'import_path': 'chatterbot.logic.BestMatch',
         'default_response': 'I am sorry, but I do not understand.',
         'maximum_similarity_threshold': 0.95}])
    english_bot.read_only = True
    return str(english_bot.get_response(userText))
 

if __name__ == "__main__":
    
    app.run()
