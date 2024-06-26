from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from bson.objectid import ObjectId
import db
import sys
import boto3
import os
import video

s3_client = boto3.client('s3', region_name="us-east-2")
app = Flask(__name__)
CORS(app)

def populate_users():
    usernames = [
        "Rich",
        "Pedro",
        "Vara",
        "Noah"
    ]
    for name in usernames:
        db.client["dev"]["users"].insert_one({"name":name,"groups":[]})

def populate_groups():
    groupnames = [
        "test1",
        "test2"
    ]
    for name in groupnames:
        db.client["dev"]["groups"].insert_one({"name":name})

def populate_users_groups():
    userids = []
    usersList = list(db.client["dev"]["users"].find())
    for user in usersList:
        userids.append(user["name"])
    
    db.client["dev"]["groups"].update_many({},{'$set': {'users': userids}})
    

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/fetchUsers')
@cross_origin()
def fetchUsers():
    usersList = list(db.client["dev"]["users"].find())
    for user in usersList:
        user["_id"] = str(user["_id"])
    return jsonify({"users":usersList})

@app.route('/fetchGroups')
@cross_origin()
def fetchGroups():
    userid = request.args.get("user_id")
    doc = db.client["dev"]["users"].find_one({'_id':ObjectId(userid)})
    groups = []
    for groupid in doc['groups']:
        group = db.client["dev"]["groups"].find_one({'_id':ObjectId(groupid)})
        group["_id"] = str(groupid)
        groups.append(group)
    return jsonify({"groups":groups})

@app.route('/fetchIndivGroup')
@cross_origin()
def fetchIndivGroup():
    group_id = request.args.get("group_id")
    doc = db.client["dev"]["groups"].find_one({'_id':ObjectId(group_id)})
    doc["_id"] = str(doc["_id"])
    meetings = list(db.client["dev"]["meetings"].find({'groupId':group_id}))
    for meeting in meetings:
        meeting["_id"] = str(meeting["_id"])
    return jsonify({"group_info":doc, "meetings":meetings})

@app.route('/createMeeting', methods=['POST'])
@cross_origin()
def createMeeting():
    args_dict = request.json
    args_dict["videolink"] = ""
    args_dict["future_tasks"] = ""
    args_dict["meetingSummary"] = ""
    args_dict["meetingProductivitySummary"] = []
    args_dict["meetingCriticism"] = ""
    args_dict["memberIndivFeedback"] = {}
    db.client["dev"]["meetings"].insert_one(args_dict)
    return jsonify({"status":"success"})

@app.route('/createUser')
@cross_origin()
def handleCreateUser():    
    return jsonify({"id":"id"})

@app.route('/getVideo')
@cross_origin()
def getVideo():  
    return send_file("files/"+request.args.get("video_path"), mimetype='video/mp4')

@app.route("/handleFileUpload", methods=['POST'])
@cross_origin()
def handleFileUpload():
    file = request.files['file']
    file.save('files/' + file.filename)
    members = ['Pedro', 'Vara', 'Noah', "Rich"]
    output = video.run_prompts("files/"+file.filename, members, 'Vara', '../Vara intro.wav')
    db.client["dev"]["meetings"].update_one(
        {'_id':ObjectId(request.args.get("meetingId"))},
        {'$set':{
            "meetingSummary":output["scribe"],
            "meetingProductivitySummary":output["meetingFeedback"],
            "future_tasks":output["futureTasks"],
            "memberIndivFeedback" : {"Vara":output["personal"]},
            "videolink":file.filename
        }}
    )
    return jsonify({"status":"OK"})

if __name__ == '__main__':
    app.run(debug=True)