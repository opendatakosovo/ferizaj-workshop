from pymongo import MongoClient
from flask import Flask, Response
from bson import json_util

app = Flask(__name__)

mongo = MongoClient()
db = mongo.kosovoprocurements
collection = db.procurements


@app.route('/')
def home():
    return "<h1>0.0.0.0:5030/string:komuna/monthly-summary/int:viti</h1>"


@app.route('/<string:komuna>/monthly-summary/<int:viti>')
def hello(komuna, viti):
    rezultati = collection.aggregate([
        {
            "$match": {
                "city": komuna,
                "viti": viti
            }
        },
        {
            "$group": {
                "_id": {
                    "muaji": {
                        "$month": "$dataNenshkrimit"
                    }
                },
                "vlera": {
                    "$sum": "$kontrata.vlera"
                },
                "qmimi": {
                    "$sum": "$kontrata.qmimi"
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "muaji": "$_id.muaji",
                "vlera": "$vlera",
                "qmimi": "$qmimi"
            }
        },
        {
            "$sort": {
                "muaji": 1
            }
        }
    ])

    resp = Response(
        response=json_util.dumps(rezultati['result']),
        mimetype='application/json')
    return resp


@app.route('/prokurimi')
def tipi_prokurimit():
    #TODO: Ekzekuto Query dhe merr te dhenat per tipet e prokurimit
    # Per Ferizaj, viti 2011
    rezultati = collection.aggregate([
        {
            "$match": {
                "city": "ferizaj",
                "viti": 2011
            }
        },
        {
            "$group": {
                "_id": {
                    "tipi": "$tipi"
                },
                "shuma": {
                    "$sum": "$kontrata.vlera"}
            }
        },
        {
            "$sort": {
                "_id.tipi": 1
            }
        },
        {
            "$project": {
                "tipi": "$_id.tipi",
                "shuma": "$shuma",
                "_id": 0
            }
        }
    ])

    resp = Response(
        response=json_util.dumps(rezultati['result']),
        mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5030)
