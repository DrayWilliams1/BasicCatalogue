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

form = cgi.FieldStorage() # gets access to the submitted form data (only instantiate one)
newUsername = form.getfirst('newUsername') # gets username from form
newPassword = form.getfirst('newPassword') # gets password from form

if newUsername!=None and newPassword!=None: # if username and password were input
    newUsername = str(newUsername)
    newPassword = str(newPassword)
    hashedPassword = hashlib.md5(newPassword).hexdigest()
    newUser = {
        'username':newUsername,
        'password':hashedPassword,
        'isAdmin':False,
        'isLoggedIn':False
    }

    tempNewUserCheck = db.users.find_one({'username':newUsername}) # checks database for pre-existence of new user
    if tempNewUserCheck == None: # no account already exists
        db.users.insert_one(newUser)
        print "<script>alert('User added to database');</script>"
    else: # an account already exists
        print "<script>alert('An account with that username already exists');</script>"

else: # username or password field are empty
    print "<script>alert('The fields cannot be empty');</script>"

print """
<html>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <head>
        <title>Assignment 4 - Signup Page</title>
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
"""
# Top shared element
print open('pageDesign.top','r').read()

# displays the admin menu if user is an admin
isAdmin = db.users.user=db.users.find_one({'username':statusName,'isAdmin':True})
if isAdmin: # the user is an admin
    print """
        <a href="adminUserPage.cgi">
          <button>Admin: Users</button>
        </a>
        <a href="adminProductPage.cgi">
            <button>Admin: Products</button>
        </a>
    """

# displaying buttons/status depending on if the user is signed in
if statusName: #user is signed in
    # display sign out button
    print """
    <a href="logoutUser.cgi">
        <button>Logout</button>
    </a>
    """
    print "<h4>"
    print "Signed in as: "+statusName
    print "</h4>"
else: # user is offline
    # display sign in button
    print '''
        <a href="loginPage.cgi">
          <button>Login</button>
        </a>
    '''
    # display status as offline
    print "<h4>"
    print "Signed in as: Offline"
    print "</h4>"

print """
    <body>
        <table cellpadding="5" cellspacing="10" align="center">
            <h3>Signup Page: Create a user account!</h3>
            <form method="post">
                <tr><th>New Username:</th><td><input type='text' name='newUsername'/></td></tr>
                <tr><th>New Password:</th><td><input type='password' name='newPassword'/></td></tr>
                <tr><td colspan="2" align="right"><input type='submit' value='Create User' name='login' /></td></tr>
            </form>
        </table>
    </body>
"""
# Bottom shared element
print open('pageDesign.bottom','r').read()
"""
</html>
"""