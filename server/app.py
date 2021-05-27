from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(host='localhost', port=27017)
db = client['test']

@app.route("/")
def index():
    print(db)
    return 'Hello, World!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)