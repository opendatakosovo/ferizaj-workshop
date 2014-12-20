from pymongo import MongoClient
from flask import Flask, render_template, Response
from bson import json_util
import argparse

app = Flask(__name__)

mongo = MongoClient()
db = mongo.kosovoprocurements
collection = db.procurements

@app.route('/')
def home():
	return "<h1>0.0.0.0:5030/string:komuna/monthly-summary/int:viti</h1>"

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

    # Define the arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to: [%(default)s].')
    parser.add_argument('--port', type=int, default=5030, help='Port to listen to: [%(default)s].')
    parser.add_argument('--debug', action='store_true', default=True, help='Debug mode: [%(default)s].')

    # Parse arguemnts and run the app.
    args = parser.parse_args()
    app.run(debug=args.debug, host=args.host, port=args.port)

