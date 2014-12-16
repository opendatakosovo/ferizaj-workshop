import csv
from pymongo import MongoClient

mongo = MongoClient()
db = mongo.ferizaji
collection = db.tabela


def lexo_file():
    with open("data/test.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            emri = row[0]
            mbiemri = row[1]
            qyteti = row[2]
            rezultati = {"emri": emri,
                "mbiemri": mbiemri,
                "qyteti": qyteti
                }
            print rezultati
            collection.insert(rezultati)
lexo_file()
