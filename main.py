#!/bin/python3
from flask import Flask, request
import pymongo, json
from bson import json_util, ObjectId

# New mongo DB client connection
mongo_db_conn = pymongo.MongoClient("mongodb://localhost:27017/")

# DB Name is filedtest
database = mongo_db_conn["filedtest"]

# collection is test
mongo_collection = database["test"]

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

    # insert the data to collection
    output = mongo_collection.insert_one(request_data)

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

    # generate query for unsetting the audio file
    query = {"audioFileType": audioFileType, "$set": request_data["audioFileMetadata"]}

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

# runs the app on port 3000
app.run("localhost",3000)
