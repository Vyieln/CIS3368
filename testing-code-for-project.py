import mysql.connector
from mysql.connector import Error
import random

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
cars = [
    
    
]
#y = 1
#for x in cars:
 #   if y == x['id']:
  #      cars.remove(x)
   #     print(cars)
#cars = ['a','b','c']
#cars[0] = 'b'
#print(cars)



test = {'fname': 'tim', 'lname': 'carl'}
if 'lname' in test:
    print('in')
else:
    print('not in')
m1 = 'a'
m2 = 'b'
m3 = 'c'
m4 = 'd'
x = ('vinny',)
carl = ('id',)
tim = [m1,m2,m3,m4]
for x in tim:
    xt = (x,)
    carl = carl + xt
#print(carl)
test = "id: %s movie 1: %s movie 2: %s movie 3: %s movie 4: %s" % carl
#print(test)


movie = {"num_users": 3, "user1": 1, "user2": 2,"user3": 4}
dicts = {}
x = 1
num_users = movie["num_users"]
while x <= num_users:
    print(x)
    y = "user%s" % (x)
    print(y)
    if y in movie:
        dicts[y] = movie[y]
    x = x + 1
print("test",dicts)

norm_str = ""  #id = [1,2,4]
ids = [1,2,4]
x = 1
while x <= num_users:
    print(x , " - " , num_users)
    if (num_users - x != 0):
        num = "%s," % (str(ids[x - 1]))
        norm_str += num
    else: 
        norm_str += str(ids[x - 1])
    print(norm_str)
    x = x + 1
print(norm_str)

query = "SELECT * FROM movielist WHERE friendid in (%s)" % (norm_str)
print(query)
connection = create_connection("cis3368.cba7r5iszeox.us-east-2.rds.amazonaws.com", "admin", "PogPogAnthony124", "CIS3368db")
cursor = connection.cursor(dictionary=True)
cursor.execute(query)
rows = cursor.fetchall()
results = []
for user in rows:
    results.append(user)
print(results)
movies = []
f = 1
moviesnum = 10
for x in rows:
    y = 1
    print(f)
    while y <= 10:
        movie = "movie%s" % (y)
        if x[movie] != "none":
            movies.append(x[movie])
        y = y + 1
    f = f + 1
print(movies)
print(movies[random.randint(0,(len(movies)- 1))])


query = "SELECT * FROM selected WHERE id = 1"
cursor = connection.cursor(dictionary=True)
cursor.execute(query)
rows = cursor.fetchall()
print(rows[0]['list'])
    
#
