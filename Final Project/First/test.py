import json
test = [
  {
    "firstname": "John", 
    "id": 1, 
    "lastname": "Perez"
  }, 
  {
    "firstname": "Timmy", 
    "id": 2, 
    "lastname": "Johnson"
  }, 
  {
    "firstname": "Alex", 
    "id": 3, 
    "lastname": "Arredondo"
  }, 
  {
    "firstname": "test", 
    "id": 4, 
    "lastname": "test"
  }
]
lol = {}
lol["user1"] = "1"
y = '{"user1" : "1"}'
print(y)
print(json.loads(y))

fen = {}
x = 0
count = 0
# for user in test:
#    print(test[x]['firstname'])
#    x = x + 1
#    count = count + 1
#    user = "user%s" % (x)
#    fen[user].append(test[x]['id'])
#   print(fen) 
