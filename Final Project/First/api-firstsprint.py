import datetime
import time
import flask
from flask import jsonify
from flask import request, make_response
import mysql.connector
from mysql.connector import Error

# setting up an application name
app = flask.Flask(__name__)
app.config["DEBUG"] = True

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def addusers():
    print("test")
def addmovie():
    print("test")
def choosemovie():
    print("test")
    
def menu():

    x = 'continue'

    while x == 'continue':
        print('a - Add User')
        print('b - Add Movie')
        print('c - Choose Movie')
        print("------------------------------------")
        option = input('Enter option: ')

        if option.lower() == 'a':
            print('Option a was chosen')
            print("------------------------------------")
            store()
        if option.lower() == 'b':
            print('Option b was chosen')
            print("------------------------------------")
            display()
            delete()
        if option.lower() == 'c':
            print('Option c was chosen')
            print("------------------------------------")
            display()
        if option.lower() == 'q':
            x = 'exit'



cars = [
    {'id': 0,
    'fname': 'Karen',
    'lname': 'Johnson'},
    {'id': 1,
    'fname': 'Pan',
    'lname': 'Johnson'},
    {'id': 2,
    'fname': 'Alexander',
    'lname': 'persen'},
    {'id': 3,
    'fname': 'Jen',
    'lname': 'Bell'},
    
]






@app.route("/", methods=["GET"]) # default url without any routing as GET request
def home(): 
    return "<h1> WELCOME TO OUR FIRST API! </h1>"

@app.route('/api/cars/all', methods=["GET"]) #endpoint to get all the cars
def api_all():
    return jsonify(cars)

@app.route('/api/cars',methods=['GET']) # endpoint to get a single car by id
def api_id():
    if 'id' in request.args: # only if an id is provided as an argument proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID provided!'
    
    results = [] # resulting car(s) to to return
    for car in cars:
        if car['id'] == id:
            results.append(car)
    return jsonify(results)

@app.route('/api/users',methods=['GET']) #api to get a user from teh db table in AWS b id as a JSON response
def api_users_id():
    if 'id' in request.args: # only if an id is provided as an argument proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID provided!'

    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM users"
    cursor.execute(sql)
    rows = cursor.fetchall()
    results = []

    for user in rows:
        if user['id'] == id:
            results.append(user)
    return jsonify(results)
    
#-------------------------
# Example to use POST as your method type, sending parameters as payload from POSTMAN (raw, JSON)
@app.route('/post-example', methods=['POST'])
def post_example():
    request_data = request.get_json()
    newid = request_data['id']
    newfname = request_data['fname']
    newlname = request_data['lname']
    cars.append({'id': newid, 'fname': newfname, 'lname' : newlname}) #adding a new car to my car collection on the server.
    #IF I go check the /api/cars/all route in the browser now, I should see this car added to the returned JSON list of cars
    return 'POST REQUEST WORKED'

#-------    
@app.route('/api-delete', methods=['DELETE'])
def api_delete():
    request_data = request.get_json()
    delid = request_data['id']
    for x in cars:
        if delid == x['id']:
            cars.remove(x)
    return 'DELETE REQUEST WORKED'
        
@app.route('/api/api-update',methods=['PUT'])
def api_update():
    request_data = request.get_json()
    updid = request_data['id']
    updfname = request_data['fname']
    updlname = request_data['lname']
    y = 0
    for x in cars:
        if updid == x['id']:
            cars[y] = {'id': updid , 'fname': updfname, 'lname': updlname }
        y = y + 1
    return 'PUT REQUEST WORKED'
    #use cars.insert()

#Adding a user to my database of users
@app.route('/api/adduser', methods=['POST'])
def adduser_db():
    request_data = request.get_json()
    addfname = request_data["fname"]
    addlname = request_data["lname"]
    #parsing the year, month, date from the user input
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    query = "INSERT INTO friend (firstname, lastname) VALUES ('"+addfname+"','"+addlname+"')"
    execute_query(connection, query)  
    return 'ADD USER REQUEST WORKED'
    #check my table in mySQL Workbench to verify the user has been added

# Delete a user from the database
@app.route('/api/deleteuser',methods=['DELETE'])
def deleteuser_db():
    # takes the data from the user and takes in the "id" field
    request_data = request.get_json()
    delid = request_data["id"]

    # Create a connection with the database by providing the address,name, and password
    # Also write the SQL code in order to give instructions to the database
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    query = "DELETE FROM friend WHERE id = %s" % (delid)
    execute_query(connection,query)
    return 'DELETE USER REQUEST WORKED'

@app.route('/api/updateuser',methods=['PUT'])
def updateuser_db():
    request_data = request.get_json()
    upid = request_data["id"]
    upfname = request_data['fname']
    uplname = request_data['lname']
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    query = "UPDATE friend SET firstname = '"+upfname+"', lastname = '"+uplname+"' WHERE id = %s" % (upid)
    execute_query(connection,query)
    return 'UPDATE USER REQUEST WORKED'



app.run()

# Day 1 -----------------------------------------------------------------------------------------
# Created some end points for the api (creating a user, deleting a user, updating a user)
# I also created some endpoints that would create the user in the database and the other CRUDs 
# Made sure that the database worked good with the code and i didn't receive any errors
# the errors that I did get, i made sure to fix them right away.
# Update function in browser (not database):
# decided to create a for statement that will find the matching id that was provided by the user
# and update the information once the for loop finds that specified user. I also did the same
# for the delete user.
# -----------------------------------------------------------------------------------------------