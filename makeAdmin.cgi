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
makeAdmin = storage.getfirst('set') # gets status of whether to set or unset as an admin
adminAccountExists = db.users.find_one({'username':accountName,'isAdmin':False})
nAdminAccountExists = db.users.find_one({'username':accountName,'isAdmin':True})
if makeAdmin != None: # the user wants to set as an admin
    if adminAccountExists != None: # if user exists in db (and is not an admin)
        db.users.update_one({'username':accountName},{'$set':{'isAdmin': True}}) # sets admin flag to true
        print "Success: "+accountName+" is now an admin"
    else:
        print "Unsuccessful: User is already an admin"
else: # the user wants to unset as an admin
    if nAdminAccountExists != None: # if user exists in db (and is an admin)
        db.users.update_one({'username':accountName},{'$set':{'isAdmin': False}}) # sets admin flag to true
        print "Success: "+accountName+" is no longer an admin"
    else:
        print "Unsuccessful: User is already not an admin"