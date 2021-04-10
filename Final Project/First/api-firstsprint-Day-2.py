import datetime
import time
import flask
from flask import jsonify
from flask import request, make_response
import mysql.connector
from mysql.connector import Error
import random
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




car = []
def databasedata():
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    query = "SELECT * FROM friend"
    dbdata = execute_read_query(connection, query)
    for row in dbdata:
        results = {"id":row[0], "fname":row[1], "lname":row[2]}
        car.append(results)
    return car
cars = databasedata()






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
    databasedata()
    request_data = request.get_json()
    print(request_data)

    addfname = request_data["fname"]
    if "lname" in request_data:
        addlname = request_data["lname"]
    else:
        print('Last Name was not provided')
        addlname = ""
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
@app.route('/api/movies/add', methods=['POST'])
def usermovies():
    request_data = request.get_json()
    print(request_data)
    fid = request_data['fid']
    if 'movie1' in request_data:
        movie1 = request_data['movie1']
    else:
        movie1 = "none"
    if "movie2" in request_data:
        movie2 = request_data["movie2"]
    else:
        movie2 = 'none'
    if "movie3" in request_data:
        movie3 = request_data['movie3']
    else:
        movie3 = 'none'
    if "movie4" in request_data:
        movie4 = request_data['movie4']
    else:
        movie4 = 'none'
    if "movie5" in request_data:
        movie5 = request_data['movie5']
    else:
        movie5 = 'none'
    if "movie6" in request_data:
        movie6 = request_data['movie6']
    else:
        movie6 = 'none'
    if "movie7" in request_data:
        movie7 = request_data['movie7']
    else:
        movie7 = 'none'
    if "movie8" in request_data:
        movie8 = request_data['movie8']
    else:
        movie8 = 'none'
    if "movie9" in request_data:
        movie9 = request_data['movie9']
    else:
        movie9 = 'none'
    if "movie10" in request_data:
        movie10 = request_data['movie10']
    else:
        movie10 = 'none'
    
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    query = "INSERT INTO movielist (movie1, movie2, movie3, movie4, movie5, movie6, movie7, movie8, movie9, movie10,friendid) VALUES ('"+movie1+"','"+movie2+"','"+movie3+"','"+movie4+"','"+movie5+"','"+movie6+"','"+movie7+"','"+movie8+"','"+movie9+"','"+movie10+"',%s)" % (fid)
    print(query)
    execute_query(connection,query)
    return 'MOVIE LIST REQUEST WORKED'




@app.route('/api/movies/all', methods=['GET'])
def show_movies():
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM movielist"
    cursor.execute(sql)
    rows = cursor.fetchall()
    results = []

    for user in rows:
        results.append(user)

    return jsonify(results)
@app.route('/api/movies',methods=['GET'])
def user_movies():
    if 'id' in request.args: # only if an id is provided as an argument proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID provided!'

    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM movielist"
    cursor.execute(sql)
    rows = cursor.fetchall()
    results = []

    for user in rows:
        if user['friendid'] == id:
            results.append(user)
    return jsonify(results)

@app.route('/api/movies/insert', methods=['POST'])
def norm_str():
    ids = []
    request_data = request.get_json()
    print(request_data)
    num_users = request_data['num']
    """
    if "user1" in request_data:
        User1 = request_data['user1']
    if "user2" in request_data:
        User2 = request_data['user2']
    if "user3" in request_data:
        User3 = request_data['user3']
    """
    x = 1
    while x <= num_users:
        print(x)
        y = "user%s" % (x)
        print(y)
        if y in request_data:
            ids.append(request_data[y])
        x = x + 1
    norm_str = ""  #id = [1,2,4]
    x = 1
    while x <= num_users:
        if (num_users - x != 0):
            num = "%s," % (str(ids[x - 1]))
            norm_str += num
        else: 
            norm_str += str(ids[x-1])
        x = x + 1
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    query = "UPDATE selected SET list = '%s' WHERE id = 1" % (norm_str) 
    execute_query(connection,query)

    return 'INSERT USERS INTO DATABASE WORKED'


@app.route('/api/movies/randompick', methods=['GET'])
def random_movie():
    """
    ids = []
    request_data = request.get_json()
    print(request_data)
    num_users = request_data['num']
    if "user1" in request_data:
        User1 = request_data['user1']
    if "user2" in request_data:
        User2 = request_data['user2']
    if "user3" in request_data:
        User3 = request_data['user3']
    x = 1
    while x <= num_users:
        print(x)
        y = "user%s" % (x)
        print(y)
        if y in request_data:
            ids.append(request_data[y])
        x = x + 1
    norm_str = ""  #id = [1,2,4]
    x = 1
    while x <= num_users:
        if (num_users - x != 0):
            num = "%s," % (str(ids[x - 1]))
            norm_str += num
        else: 
            norm_str += str(ids[x])
        x = x + 1
    """
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    query = "SELECT * FROM selected WHERE id = 1"
    query = "SELECT * FROM selected WHERE id = 1"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    rows = cursor.fetchall()
    norm_strs = rows[0]['list']

    query = "SELECT * FROM movielist WHERE friendid in (%s)" % (norm_strs)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    rows = cursor.fetchall()
    movies = []
    for x in rows:
        y = 1
        while y <= 10:
            movie = "movie%s" % (y)
            if x[movie] != "none":
                movies.append(x[movie])
            y = y + 1
    randompick =  movies[random.randint(0,(len(movies)- 1))]
    return randompick





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
# Day 2 -----------------------------------------------------------------------------------------
# Added more endpoints to the code. the firsts ones being the update and delete for the database 
# For the delete endpoint they must provide the id of the user as well for the update one
# Created the the database for the movies, created 10 fields for the movies and 1 for the friendid
# the friend ID must be provided. The first route for the movies will be to add movies to the user
# created POST that will ask for the friendid and then the movies that they want to add. if they 
# don't provided names for the rest of the fields (ex. 1-3: movies, 4-10: no movies provided)
# then it will fill the fields with "none". I then created two more 'GET' endpoints that will 
# display the infomration from the table in json form on the web. the first one will display
# all of the information from the table. Then the second 'GET' will show a specified user movies
# only. Lastly I created the endpoints to select a random movie from the database. First I created
# a 'POST' endpoint that will ask for the 'friendid' of the users that were selected. So if users
# (1,2,4) were selected then it would be {"user1": 1, "user2": 2, "user3": 4} this will be sent
# through postman. After that I created some loops that would create a list with the users ID only
# then it would convert it into a string ("1,2,4"). After that the string will be sent to the 
# database in a one line database. The last endpoint is where is the random movie is picked
# When you enter "127.0.0.1:5000/api/movies/randompick" it will display the result. This works
# by firstly taking the single string data ("1,2,4") from the database and inserting into a query
# that asks the table with all of the movies to "SELECT * from movieslist where ID in (1,2,4)' 
# returning only the rows from those with the ids specified. After that I created a loop that 
# run through all of the rows provided and insert all of the movies that were selcted into a 
# list. I used an if statement in order to not insert the "none" responses for the fields that 
# have no movies. I also imported the random module in order to select a random number from 
# the range of 0 and the length of the list with the movies
# -----------------------------------------------------------------------------------------------