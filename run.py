from pymongo import MongoClient
from flask import Flask, render_template, Response
from bson import json_util

app = Flask(__name__)

mongo = MongoClient()
db = mongo.kosovoprocurements
collection = db.procurements

@app.route('/<string:komuna>/monthly-summary/<int:viti>')
def hello(komuna,viti):
    rezultati = collection.aggregate([{
	        "$match":{
	            "city":komuna,
	            "viti":viti
	            }
	        },
	    {
	        "$group":{
	           "_id": {
	                "muaji":{
	                    "$month":"$dataNenshkrimit"
	                }
	            },
	            "vleraKontrates":{
	                "$sum":"$kontrata.vlera"
	            },
	            "qmimi":{
	                "$sum":"$kontrata.qmimi"
	            }
	        }
	    },
	    {
	        "$project":{
	            "_id":0,
	            "muaji" :"$_id.muaji", 
	            "vlera":"$vleraKontrates", 
	            "qmimi":"$qmimi"
			}
	    },
	    {
	        "$sort":{
	            "muaji":1
	        }
	    }
	])

    return Response(response=json_util.dumps(rezultati), mimetype="application/json")

if __name__ == '__main__':
    app.run(debug=True)
