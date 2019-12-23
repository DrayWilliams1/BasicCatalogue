#!/usr/bin/python
import cgi, os # For environment data and helpers
import hashlib # For basic password security
from pymongo import MongoClient # For MongoDB connections
import cgitb #Traceback
cgitb.enable()
'''
    Name: Drayton Williams
'''
# Details to access MongoDB
username='dw15we'
passwd='5925342'
client=MongoClient('mongodb://'+username+':'+passwd+'@127.0.0.1/'+username)
db=client[username]

print "Content-Type: text/html"
print

storage = cgi.FieldStorage() # gets access to the submitted form data (only instantiate one)
accountName = storage.getfirst('accountName') # gets username from form

accountExists = db.users.find_one({'username':accountName})

if accountExists != None: # if product exists in db
    db.users.remove({'username':accountName}) # removes product from database
    print "Success: "+accountName+" has been removed from database"
else:
    print "Unsuccessful: User does not exist in database"
