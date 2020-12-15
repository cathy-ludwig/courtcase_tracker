# app.py
from flask import Flask, request, jsonify
from get_cases import query_cases, connect_to_db
from main import get_data, update_db
from datetime import datetime
import json
app = Flask(__name__)

@app.route('/cases/', methods=['GET'])
def cases():
    return query_cases(connect_to_db(), 'test')

@app.route('/adddata/', methods=['GET'])
def adddata():
    # Retrieve the name from url parameter
    date_time_str = request.args.get("date", None)
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')
    table_rows = get_data(date_time_obj.strftime('%Y/%m/%d'))
    #update_db(connect_to_db(), table_rows)
    return json.dumps(table_rows)

@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
