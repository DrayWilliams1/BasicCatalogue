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

#If the user is successfully logging in, we need to create a new
#session id, put that into the database (under the correct user),
#and pass the same session id to the user via cookie
#Finally, redirect back to the original page
def create_session(username):
    sid=uuid.uuid1().hex
    db.users.update_one({'username':username},{'$set':{'usid':sid}})
    print "Set-Cookie: user="+username
    print "Set-Cookie: usid="+sid
    print "Location: ./mergeLoad.cgi" #The redirect
    print
    exit()

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

def check_valid():
    form = cgi.FieldStorage() # gets access to the submitted form data (only instantiate one)
    username = form.getfirst('username') # gets username from form
    password = form.getfirst('password') # gets password from form

    if username!=None and password!=None: # if username and password were input
        username = str(username)
        password = str(password)
        hashedPassword = hashlib.md5(password).hexdigest()
        # checks database for existence of entered user
        user=db.users.find_one({'username':username,'password':hashedPassword})
        if user==None: # user does not exist in database
            print "Location: ./loginPage.cgi" #The redirect
            #exit()
        else: # user exists in database
            # updating user in database to be logged in
            db.users.update_one({'username':username},{'$set': {'isLoggedIn': True}})
            # call cookie creating function
            create_session(username)
            exit()

print "Content-Type: text/html"

# If already logged in, page will automatically redirect to main page
statusName = check_logged_in()
if statusName:
    print "Location: ./productListingPage.cgi" #The redirect 
isValid = check_valid()
print

print """
<html>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <head>
        <title>Assignment 4 - Login Page</title>
        <link rel="stylesheet" type="text/css" href="style.css">
        <style>
            th {
                text-align: right;
            }
            h3 {
                text-align: center;
            }
        </style>
    </head>
    <body>
"""
# Top shared element
print open('pageDesign.top','r').read()

print """
    <table cellpadding="5" cellspacing="10" align="center">
        <h3>Login Page: Using MongoDB!</h3>
        <form method="post">
            <tr><th>Username:</th><td><input type='text' name='username'/></td></tr>
            <tr><th>Password:</th><td><input type='password' name='password'/></td></tr>
            <tr><td colspan="2" align="right"><input type='submit' value='Login' name='login' /></td></tr>
        </form>
    </table>
"""
# Bottom shared element
print open('pageDesign.bottom','r').read()
"""
    </body>
</html>
"""