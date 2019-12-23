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
productName = storage.getfirst('productName') # gets username from form

productExists = db.products.find_one({'name':productName})

if productExists != None: # if product exists in db
    db.products.delete_many({'name':productName}) # removes product from database
    print "Success: "+productName+" has been removed from database"
else:
    print "Unsuccessful: Product does not exist in database"
