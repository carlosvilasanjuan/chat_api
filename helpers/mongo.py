from pymongo import MongoClient

client = MongoClient()
db = client.get_database("chat")


def insert_data(data):
    curs = db.messages.insert_one({'name':f'{data}'})
    return {"_id": curs.inserted_id}

def get_id(data):
    curs = db.messages.find({'name':data})
    return list(curs)