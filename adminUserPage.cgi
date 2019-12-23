#!/usr/bin/python
import cgi, os #For environment data and helpers
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

# If user is not an admin (or not logged in), page will automatically redirect to main page
notAdmin = db.users.user=db.users.find_one({'username':statusName,'isAdmin':False})
if notAdmin or statusName==None:
    print "Location: ./productListingPage.cgi" #The redirect 
print

print """
<html>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <head>
        <title>Assignment 4 - Product Administration</title>
        <link rel="stylesheet" type="text/css" href="style.css">
        <script>
            // makes a user an administrator
            function makeAdmin(accountName) {
                req=new XMLHttpRequest();
                req.onreadystatechange=function(){
                    if (this.readyState==4 & this.status==200) {
                        alert(this.response);
                    }
                };
                req.open("GET","makeAdmin.cgi?accountName="+accountName+"&set=yes");
                req.send();
            }

            // removes user admin permissions
            function removeAdmin(accountName) {
                req=new XMLHttpRequest();
                req.onreadystatechange=function(){
                    if (this.readyState==4 & this.status==200) {
                        alert(this.response);
                    }
                };
                req.open("GET","makeAdmin.cgi?accountName="+accountName);
                req.send();
            }

            // removes product database
            function removeFromDatabase(accountName) {
                req=new XMLHttpRequest();
                req.onreadystatechange=function(){
                    if (this.readyState==4 & this.status==200) {
                        alert(this.response);
                    }
                };
                req.open("GET","removeDatabaseUser.cgi?accountName="+accountName);
                req.send();
            }
        </script>
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
<body class="allListings">
    <h1>User Administration Page</h1>
    <p>Allowing users to view, edit, or remove users from database</p>
    <h3>Current Database User Accounts</h3>
    <p>View/Remove Users below</p>
"""
    
# ------ Generating Products from database
users = db.users.find({},{'_id':False})
for record in users: # Creates and displays relevant info for each product in catalogue
    print "<h4>"+record['username']+"</h4>"
    print "<button id='setAdminButton_"+record['username']+"'>Set "+record['username']+" as an admin</button>"
    print "<button id='unsetAdminButton_"+record['username']+"'>Unset "+record['username']+" as an admin</button>"
    print "<button id='removeButton_"+record['username']+"'>Remove "+record['username']+" from database</button>"
    # Adding event listener to set admin button via javascript
    print "<script>document.getElementById('setAdminButton_"+record['username']+"').addEventListener('click',function(){makeAdmin('"+record['username']+"');});</script>"
    # Adding event listener to unset admin button via javascript
    print "<script>document.getElementById('unsetAdminButton_"+record['username']+"').addEventListener('click',function(){removeAdmin('"+record['username']+"');});</script>"
    # Adding event listeners to remove buttons via javascript
    print "<script>document.getElementById('removeButton_"+record['username']+"').addEventListener('click',function(){removeFromDatabase('"+record['username']+"');});</script>"

# Bottom shared element
print open('pageDesign.bottom','r').read()
"""
    </body>
</html>
"""