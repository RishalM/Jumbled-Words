from re import A
from flask_moment import Moment
import random
from crypt import methods
from flask import Flask, render_template, request, redirect, flash
import os
import pymongo
app = Flask("Jumbled Words")
moment = Moment(app)
if os.environ.get("MONGO_URI") == None: #we are running the code on our computer. If we run on our computer, os.environ.get("MONGO_URI") will be none
    file = open("connectionString.txt","r")
    content = file.read().strip()
    file.close()
else: # we are running this code on Heroku's computer. Here, os.environ.get("MONGO_URI") will not be none -- instead it will be the connection string.
    content = os.environ.get("MONGO_URI")
client = pymongo.MongoClient(content)
database = client["JumbledWords"]
collection = database["AllWords"]

@app.route("/", methods = ["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        addwordinfo = request.form
        wordtoadd = addwordinfo['wordtoadd'].lower()
        addwordlist = list(wordtoadd)
        random.shuffle(addwordlist)
        jumbledword = "".join(addwordlist)
        print(jumbledword)
        record = {"originalWord":wordtoadd,"jumbledword":jumbledword}
        collection.insert_one(record)
        return redirect ("/")

@app.route("/play", methods = ["GET","POST"])
def play():
    if request.method == "GET":
        records = collection.find()
        words = []
        for each in records:
            words.append(each)
        random.shuffle(words)
        return render_template("play.html",words = words[0:5])
    else:
        numberofcorrectanswers = 0
        alluseranswers = request.form.getlist("answer")
        allcorrectanswers = request.form.getlist("question")
        for i in range(0,len(allcorrectanswers),1):
            if alluseranswers[i] == allcorrectanswers[i]:
                numberofcorrectanswers = numberofcorrectanswers + 1
        print(numberofcorrectanswers,"out of",len(allcorrectanswers))
        lenofcorrectanswers = len(allcorrectanswers)
        return render_template("result.html",numberofcorrectanswers=numberofcorrectanswers,lenofcorrectanswers = lenofcorrectanswers)

        



        
    











app.run(debug=True)