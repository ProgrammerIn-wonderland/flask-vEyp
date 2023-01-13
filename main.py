import flask
import time
import json

# Initialize
jsoncache = {}
app = flask.Flask("SocialCreditSystem") 

# read file
filedb = open("jsondb.json", 'r+') 
jsoncache = json.load(filedb)

def commit(student, datatype, data):
    # Initialize student if not already initialized
    if student not in jsoncache: 
        jsoncache[student] = {}

    jsoncache[student][datatype][time.time()] = data # Format, Student.[sports, tournament].time

    # Write data to db
    filedb.seek(0) 
    json.dump(jsoncache, filedb, indent=4)
    return {"statuscode": "success"}
    
    

def register(args):
    if ("sport" in args): # Sports Handler
        if (args["sport"] in ["basketball", "baseball", "football", "soccer", "volleyball", "wrestling"]):
            return commit(args["student"], "sports", {"role": args["action"], "sport": args["sport"]})
        else: 
            return {"error": "invalid sport"}

    if ("tournament" in args): # Tournament
        if (args["tournament"] in ["chess", "robotics", "business", "academic", "esports"]):
            return commit(args["student"], "tournament", {"role": args["action"], "category": args["tournament"]})
        else: 
            return {"error": "invalid tournament"}
    
    elif (args["action"] == "grade"): # Grades Handler
        return commit(args["student"], "grades", {"quarter": args["quarter"], "grades":{"English": args["english"],"Math": args["math"],"Science": args["science"],"History": args["History"]}})
    else:
        return {"error": "No Sport or Event specified"}

@app.route('/api')
def api():
    args = flask.request.args
    try:
        if (args["action"] == "attend" or args["action"] == "play" or args["action"] == "grade"): # Initial argument handler for actions that commit to DB
            student=int(flask.request.args["student"])
            action=str(flask.request.args["action"])
            return flask.jsonify(register(args)) # Pass return responsibility to whatever runs next
    
        if (flask.request.args["action"] == "pull"): # Handles requests looking to pull from DB
            return flask.jsonify(jsoncache)
    
    except Exception as e: # A catch all
        print(e)
        return flask.jsonify({"error": "Failed to parse data"})
    
    return flask.jsonify({"status": "default"})

@app.route('/')
def index():
    return flask.render_template("index.htm")
app.run(host='0.0.0.0', port=105)




