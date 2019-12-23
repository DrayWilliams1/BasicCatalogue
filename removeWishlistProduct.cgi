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

def check_logged_in():
    if os.environ.has_key('HTTP_COOKIE'):
        user=None #Assume doesn't exist
        usid=None # until proven otherwise
        cookies=os.environ['HTTP_COOKIE'].split(';')
        for cookie in cookies:
            if cookie.split('=')[0].strip()=='user':
                user=cookie[cookie.find('=')+1:] #Is this one understandable?
            elif cookie.split('=')[0].strip()=='usid':
                usid=cookie[cookie.find('=')+1:]
        if user and usid: #If we have cookies for a username/sesionid
            rec=db.users.find_one({'username':user,'usid':usid})
            if rec!=None: #If the database records match the user
                return user #I know, a little weird to not return True
    return None
print "Content-Type: text/html"
statusName=check_logged_in()
print

storage = cgi.FieldStorage() # gets access to the submitted form data (only instantiate one)
productName = storage.getfirst('productName') # gets username from form

productExists = db.products.find_one({'name':productName,'owner':statusName})

if productExists != None: # if product exists in db
    db.products.remove({'name':productName,'owner':statusName}) # removes product from database
    print "Success: "+productName+" has been removed from "+statusName+ "'s wishlist"
else:
    print "Unsuccessful: Product does not exist in "+statusName+ "'s wishlist"