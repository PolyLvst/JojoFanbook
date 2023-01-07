import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask,request,jsonify,render_template
from pymongo import MongoClient
import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get('MONGO_DB_URI')
DB_NAME =  os.environ.get('DB_NAME')

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fans',methods=['POST'])
def post_fans():
    x = datetime.datetime.now()
    year =x.strftime("%G")
    comment_receive = request.form['comment_give']
    username_receive = request.form['username_give']
    doc = {
        'username': username_receive,
        'comments': comment_receive,
        'year': year
    }
    db.webfans.insert_one(doc)
    return jsonify({'msg': 'Oke thanks'})

@app.route('/fans',methods=['GET'])
def get_fans():
    comments = list(db.webfans.find({},{'_id':False}))
    return jsonify({
        'msg': 'Okay',
        'fans_comments': comments
    })

if __name__=='__main__':
    app.run('0.0.0.0',5000,debug=True)