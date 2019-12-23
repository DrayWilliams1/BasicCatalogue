#!/usr/bin/python
import cgi, os, uuid # For environment data and helpers
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

# Checks the header cookies for the currently logged in user
# and returns the username
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
offlineProducts = storage.getfirst('productList') # gets username from form

if offlineProducts: # if provided a list in the header
    productSplit = [x.strip() for x in offlineProducts.split(',')]
    for product in productSplit:
        mergeProduct = db.products.find_one({'name':product,'owner':statusName})

        if mergeProduct == None: # if product does not exist in server list, merge and add it to list
            newProduct = db.products.find({'name':product,'owner':'null'})
            for record in newProduct: # Will fill inserted product details with that of the basic product entry
                newProduct ={
                    'id':record['id'],
                    'name':record['name'],
                    'description':record['description'],
                    'cost':record['cost'],
                    'image':record['image'],
                    'owner':statusName
                }
            db.products.insert_one(newProduct)

            print product+" merged into server wishlist"
        else: # product already exists in server list
            print product+" already exists in server wishlist"
else:
    print "Unsuccessful: No products added to wishlist"