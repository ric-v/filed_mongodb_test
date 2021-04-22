#!/bin/python3
from flask import Flask, request
from bson import json_util
import pymongo, sys, getopt

# new flas app
app = Flask(__name__)

# 
# Create new entry in DB
# 
@app.route("/create", methods=['GET', 'POST'])
def create():
    
    '''
    sample data : 

    {"audioFileType":"song","audioFileMetadata":{"ID":1234256,"Name":"audio1","Duration":5,"UploadTime":"2020-01-02 15:00:00"}}

    '''

    # get the payload from request
    request_data = request.get_json()
    print(request_data)

    # insert the data to collection
    mongo_collection.insert_one(request_data)

    return "success"

# 
# delete entry in DB
# 
@app.route("/delete/<audioFileType>/<audioFileID>", methods=['GET', 'POST'])
def delete(audioFileType, audioFileID):
    
    '''
    sample data : 

    audioFileType = song
    audioFileID = 1234256
    
    '''

    # generate query for unsetting the audio file
    query = {"audioFileType": audioFileType}, {"$unset": {"audioFileMetadata": {"ID": audioFileID}}}

    # execute the update query
    mongo_collection.update_one(query)

    return "success"

# 
# update entry in DB
# 
@app.route("/update/<audioFileType>/<audioFileID>", methods=['GET', 'POST'])
def update(audioFileType, audioFileID):
    
    '''
    sample data : 

    {"audioFileType":"song","audioFileMetadata":{"ID":1234256,"Name":"audio1","Duration":5,"UploadTime":"2020-01-02 15:00:00"}}

    '''

    # get the payload from request
    request_data = request.get_json()

    # execute the update query
    mongo_collection.update_one({"audioFileType": audioFileType}, { "$set": request_data["audioFileMetadata"]}, upsert=True)

    return "success"

# 
# get details from DB
# 
@app.route("/get/<audioFileType>", methods=['GET', 'POST'])
def get(audioFileType):

    '''
    sample data : 

    audioFileType = song
    
    '''

    result = []
    
    # generate query for unsetting the audio file
    query = {"audioFileType": audioFileType}

    # execute the update query
    cursor = mongo_collection.find(query)

    # iterate on each entry from collection
    for entry in cursor:

        # append each entry to final list
        result.append(entry)

    return json_util.dumps(result)

# 
# get details from DB
# 
@app.route("/get/<audioFileType>/<audioFileID>", methods=['GET', 'POST'])
def getAll(audioFileType, audioFileID):
    
    '''
    sample data : 

    audioFileType = song
    audioFileID = 1234256
    
    '''

    # generate query for unsetting the audio file
    query = {"audioFileType": audioFileType, "audioFileMetadata.ID": int(audioFileID)}

    # execute the update query
    result = mongo_collection.find_one(query)
    return json_util.dumps(result)

# default arg values
port = 3000
db_url = "mongodb://localhost:27017/"
db_name = "filedtest"
collection_name = "test"

# get args from cmd line
argv = sys.argv[1:]

# get command line args 
try:
    opts, args = getopt.getopt(
        argv,
        "hpmdc:o:",
        ["port=","db=","mongodb=","--db=","--collection="]
    )
    
except getopt.GetoptError:
    sys.exit(2)

# iterate on each args and get the value for 
# command line args
for opt, arg in opts:

    if opt == '-h':
        sys.exit()

    elif opt in ("-i", "--port"):
        port = arg

    elif opt in ("-m", "--mongodb"):
        db_url = arg

    elif opt in ("-d", "--db"):
        db_name = arg

    elif opt in ("-c", "--collection"):
        collection_name = arg

# New mongo DB client connection
mongo_db_conn = pymongo.MongoClient(db_url)

# DB Name is filedtest
database = mongo_db_conn[db_name]

# collection is test
mongo_collection = database[collection_name]

# runs the app on port 3000
app.run("localhost", port)
