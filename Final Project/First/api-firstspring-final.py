import datetime
import time
import flask
from flask import jsonify
from flask import request, make_response, render_template
import mysql.connector
from mysql.connector import Error
import random


# setting up an application name
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# creates the connection with the AWS database by taking the user database name, username, password, and the host name
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        # requries the host name, user name, password, and the database name in order to connect to the AWS database
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        # if it connects successfully then it display this message for the user
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# Takes in the users query provided by the user and executes it by first connecting to the database and then executing the given query
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully") # If the query is correct and runs then it returns this message
    except Error as e:
        print(f"The error '{e}' occurred")

# First taking the the query that instructs the database to return data to display then it returns the given data
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred") # if there is an error it will display this message




friend = [] # empty list to hold user information

def databasedata():
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    query = "SELECT * FROM friend"
    dbdata = execute_read_query(connection, query)
    for row in dbdata:
        results = {"id":row[0], "fname":row[1], "lname":row[2]}
        friend.append(results)
    return friend

friends = databasedata() # variable contains that information




# default url without any routing as GET request / returns the html code to the default url
@app.route("/", methods=["GET"])
def home(): 
    return "<h1> WELCOME TO MY RANDOM MOVIE SELECTOR API! </h1>"

#endpoint to get all the cars
@app.route('/api/friends/all', methods=["GET"]) 
def api_all():

    # creates connection with my data base
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM friend" # query to select everything from the table friend
    cursor.execute(sql)
    rows = cursor.fetchall()
    results = []

    # for statement to append the each row from the table into the list results
    for user in rows:
        results.append(user)

    return jsonify(results) # returns friends in json format

# endpoint to get a single car by id 
@app.route('/api/friends',methods=['GET'])
def api_id():
    if 'id' in request.args: # only if an id is provided as an argument proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID provided!'

    # creates a connection with the AWS database
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM friend" # selects everything from
    cursor.execute(sql)
    rows = cursor.fetchall()
    results = []

    # for loop to find the id that matches the one provided
    # goes through the list provided from the database
    for user in rows:
        if user['id'] == id:
            results.append(user)
    return jsonify(results)



#----------- Movie Selector -----------

# Example to use POST as your method type, sending parameters as payload from POSTMAN (raw, JSON)
# Here using the POSTMAN, the user will send in the data to the endpoint then it will append that data to the friends list
# displaying the data in the url /post-example where it is visible


# ------- Add User -----------------
# Adding a user to my database table named friend
@app.route('/api/db/adduser', methods=['POST'])
def adduser_db():

    # request data from the user in order to input it into the database
    # here it requires the first name and last name
    # but if the lname is not provided it returns that the last name was not provided 
    # then it leaves the lname blank only having a fname for the user
    request_data = request.get_json()
    addfname = request_data["fname"]
    if "lname" in request_data:
        addlname = request_data["lname"]
    else: # if the user does not provide a last name
        print('Last Name was not provided')
        addlname = ""

    # creates the connection with the my AWS database
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    # Creates a query in order to inser the values given from the user into the friend table, the user id is not need since 
    # it has the auto incremenet option
    query = "INSERT INTO friend (firstname, lastname) VALUES ('"+addfname+"','"+addlname+"')"
    execute_query(connection, query)  # executes the query and places the values into the database
    return 'ADD USER REQUEST WORKED' # returns string to make sure it worked


# -------- Delete user -------------
# Delete a user from the databas named friend
@app.route('/api/deleteuser',methods=['DELETE'])
def deleteuser_db():
    # takes the data from the user and takes in the "id" field
    request_data = request.get_json()
    delid = request_data["id"]

    # Create a connection with the database by providing the address,name, and password
    # Also write the SQL code in order to give instructions to the database
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    query = "DELETE FROM friend WHERE id = %s" % (delid) # deletes from the friend table given where the id matches
    execute_query(connection,query) 
    return 'DELETE USER REQUEST WORKED' # returns string to make sure it worked

# -------- Updates Info ------------
# Update a user from the database named friend
@app.route('/api/updateuser',methods=['PUT'])
def updateuser_db():
    y = "both"
    # Request data from the user in POSTMAN in order to update the information
    request_data = request.get_json()

    # requires the id, fname, and lname in order to update the information
    # if the First/last name is not provided then it sets y to a string which 
    # will alter the query to only need either the fname/lname allowing the user
    # if needed to only update one field
    upid = request_data["id"]
    if 'fname' in request_data:
        upfname = request_data['fname']
    else:
        y = "last"
    if 'lname' in request_data:
        uplname = request_data['lname']
    else:
        y = "first"

    # creates the connection between my AWS db
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    
    # different queries for the different situations 
    if y == "both":
        query = "UPDATE friend SET firstname = '"+upfname+"', lastname = '"+uplname+"' WHERE id = %s" % (upid) # will update the friend list values firstname,lastname, where the id matches the one chosen
    elif y == "first":
        query = "UPDATE friend SET firstname = '"+upfname+"' WHERE id = %s" % (upid)
    elif y == "last":
        query = "UPDATE friend SET lastname = '"+uplname+"' WHERE id = %s" % (upid)
    
    execute_query(connection,query) # executes query
    return 'UPDATE USER REQUEST WORKED' # returns string to make sure it works


# -------- Adds Movies ---------------------
# Adds a movie list to the given user
@app.route('/api/movies/add', methods=['POST'])
def usermovies():
       
    # creates a connection between the AWS db given the information needed
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")

    # First it selects all the datafrom movielist
    select_contacts = "SELECT * FROM movielist"
    contacts = execute_read_query(connection, select_contacts)
    contact_list = [0]

    # in the for loop it first starts with zero (before anything is added in the table)
    # then if for example two users are already in, so they have id: 1 and id:2
    # therefore it creates a list with the numbers (0,1,2)
    # then i created variable that will look at the last number in the list and add + 1
    # to it in order to create the next id. I did this in order to give my 'friendid' column
    # the primary key since it didn't allow me unless i took the auto_increment away from the 'id' column
    for contact in contacts:
        id = contact[0]
        contact_list.append(id)
    contacts_from_user = (contact_list[-1] + 1)
    
    # request data given by the user from POSTMAN
    request_data = request.get_json()

    # Requires the friend id / user id to be given 
    # then it allows the users to be input the movies that the want to add all the way up to 10
    # if not all movies are provided then it fill the rest with 'none' instead of blank
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
 
    # A query in order to insert the movies for the friendid into the table movielist
    query = "INSERT INTO movielist (movie1, movie2, movie3, movie4, movie5, movie6, movie7, movie8, movie9, movie10,id,friendid) VALUES ('"+movie1+"','"+movie2+"','"+movie3+"','"+movie4+"','"+movie5+"','"+movie6+"','"+movie7+"','"+movie8+"','"+movie9+"','"+movie10+"',%s,%s)" % (contacts_from_user,fid)
    execute_query(connection,query) # executes the query
    return 'MOVIE LIST REQUEST WORKED' # returns string if it worked


# -------- Displays All Users movies -------
# Displays users and their coresponding movielist
@app.route('/api/movies/all', methods=['GET'])
def show_movies():

    # first creates the connection between the aws database 
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")

    # fetches the data from the database and returns it in rows.
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM movielist"
    cursor.execute(sql)
    rows = cursor.fetchall()
    results = []

    # for loop in order to append each row to the list 'results' then it returns the returns to the 
    # endpoint /api/movies/all and displays the data when you type the url
    for user in rows:
        results.append(user)

    return jsonify(results) # returns data to url


# -------- Displays single user movies -----
# Displays a selected users movielist
@app.route('/api/movies',methods=['GET'])
def user_movies():

    # checks if an id was provided if not it returns an error and tells the user that no id was provided
    if 'id' in request.args: # only if an id is provided as an argument proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID provided!'
    # creates a connection to the AWS db
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")

    # fetches the data using the query 'sql' in order to select everything from the movielist
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT * FROM movielist" # selects all the data from the table movielist
    cursor.execute(sql)
    rows = cursor.fetchall()
    results = [] # table to hold data

    # for loop that checks the data rows to first match the id then it appends that user to the results liust
    for user in rows:
        if user['friendid'] == id:
            results.append(user) # appends data to list
    return jsonify(results) # returns the specified user data



# -------- Select Users for random movie ---
# Adds the users that were selected choose at random to a database
# this endpoint will give the user to option to select the users that want thier movies
# to be selected 
# Takes the data from the table and picks a random movie from the given users
# Instead of having two seperate endpoints one GET one POST
# I combined them and added an IF statment so i choose to post it goes to the post code
# if i choose get i gets me the else code
@app.route('/api/movies/random', methods=['GET','POST'])
def movie_selection():
    connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
    if flask.request.method == 'POST':
        ids = [] # list for the ids provided

        # request data needed for the query
        request_data = request.get_json()
        num_users = request_data['num'] # number of user that are going to be used

        # while loop that uses the number given (which is the amount of user that are going to be used)
        # then it will run that loop for that many users
        # the loop will append the user id that is going to be provided by the person that inserts the data
        # so for example if i want to only use to users i would {"num": 2, "user1": 1, "user2": 4} <-- the number that corresponds to the user(X) is going to be 
        # the id that is given to the user in the first table 

        x = 1
        while x <= num_users:
            y = "user%s" % (x)
            if y in request_data:
                ids.append(request_data[y])
            x = x + 1

        norm_str = ""  # this string is going to turn eventually to the ids of the user --> id = [1,2,4]
    
        # converts the numbers from the list into string and creates a tuple in order to insert it into the query
        # this allows the us to insert the stirng of users into the database
        # the table that we will be using will be a single row/column that only contains the string of users
        # this data will be used in the next endpoint
        x = 1
        while x <= num_users:
            if (num_users - x != 0):
                num = "%s," % (str(ids[x - 1]))
                norm_str += num
            else: 
                norm_str += str(ids[x-1])
            x = x + 1
    
        # creates the connection with the AWS database
        connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
        query = "UPDATE selected SET list = '%s' WHERE id = 1" % (norm_str)  # this query will update the 1 row/column to the string of users that was selected by the users for the movies
        execute_query(connection,query) 

        return 'INSERT USERS INTO DATABASE WORKED'
    else:
        connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")

        # this query will select that data that was inserted in the in the endpoint prior /api/movies/insert
        query = "SELECT * FROM selected WHERE id = 1"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        norm_strs = rows[0]['list']
    
        # creates the connection with the AWS database
    
        # once we recieve the string of ids that was provided by the insert endpoint 
        # we insert that string into this query that will return the data from those selected users
        query = "SELECT * FROM movielist WHERE friendid in (%s)" % (norm_strs) # inserts the string of user into the query
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        movies = []

        # this for loop will select the movies from the selected user and insert them into them into a list called movies
        # if the it says 'none' then it will not be inserted into the list
        for x in rows:
            y = 1
            while y <= 10:
                movie = "movie%s" % (y)
                if x[movie] != "none":
                    movies.append(x[movie])
                y = y + 1
    
        # this variable uses the random module to select a random number and then select a movies
        # first it takes the length of the list of movies and sets the range for number that can be selected
        # after it selects the number in the range provided it will use that number and insert itself in the movies[x]
        # to select the movie and the variable randompick will take the movie
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
# Day 3 -----------------------------------------------------------------------------------------
# removed unecessary code that didn't affect the rest of the code
# then i added the comments to describe the code and make it easier to understand why i did
# certain things. Changed the name of certain list in order for them to make more sense, since they
# were used for different things before
# Day 4 (final) ---------------------------------------------------------------------------------
# Removed more code that was not neccessary for the project
# Then For my last two endpoints which were for the movie selection, instead of having
# two, I combined them into one and made it much more easier to use. So now if i want to choose
# my users I first go to postman then i insert the body that is needed to select the users i want
# after that it we go to the same url that I just on it for post and it returns the result for the users
# that i picked. I used this https://stackoverflow.com/questions/42018603/handling-get-and-post-in-same-flask-view
# as a refrence to combine the GET and POST methods into one making much easier to read and run.
# Added more comments to describe the code a little bitter
# -----------------------------------------------------------------------------------------------