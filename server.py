from flask import Flask, render_template, request, url_for
from createObject import project, mongoDB
import json
app = Flask(__name__)

@app.route("/intialise/",methods=['POST'])
def intialiseMongoDB():
    try:
        global mongo 
        mongo = mongoDB(**request.json)
        return mongo.getdetails()
    except Exception as inst:
        print(inst)
        return "please provide mongoDBurl, mongoDBdatabase"

@app.route("/intialise/",methods=['GET'])
def getMongoDB():
    try:
        return mongo.getdetails()
    except Exception as inst:
        return "mongodb not initialised"
        

@app.route("/project/",methods=['POST'])
def addproject():
    try:
        projectname=request.json["projectname"]
        description=request.json["description"]
        organization=request.json["organization"]
        members=request.json["members"]
        p = project(projectname,description,members,organization)
        return p.getprojects()
    except Exception as inst:
        print(inst)
        return "error in request: is missing please check input json"

@app.route("/project/",methods=['GET'])
def getproject():
    """
    try:
        p = project("name","desc","mem","org")
        return p.getprojects()
    except Exception as inst:
        print inst
        return "make sure database is initialised"
    
    return p.getprojects()


"""
@app.route("/project/<projectname>",methods=['POST']) 
"""
if __name__ == "__main__":
    app.run(
        port=8000
    )
