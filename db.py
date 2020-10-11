import pymongo
import os

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
URI = "mongodb+srv://{}:{}@placement-cluster.vnhw2.mongodb.net/?retryWrites=true&w=majority".format(DB_USERNAME, DB_PASSWORD)
client = pymongo.MongoClient(URI)
db = client['placement']

def get_data():
    latest_doc = db.dump.find().sort('count', pymongo.DESCENDING)[0]
    return latest_doc['count'], latest_doc['announcements'], latest_doc['jobs']

def store_data(count, announcements, jobs):
    doc = {
        'count': count,
        'announcements': announcements,
        'jobs': jobs
    }
    db.dump.replace_one({'count': count-1}, doc)