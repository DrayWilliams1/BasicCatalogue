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
print

print """
<html>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <head>
        <title>Assignment 4 - Product Listing</title>
        <link rel="stylesheet" type="text/css" href="style.css">
        <script>
            /* Function to load stored wish list*/
            function loadList() {
                if (localStorage.getItem('wishState')) {
                    retrieveWish = JSON.parse(localStorage.getItem('wishState'));
                } else {
                    retrieveWish = [] // create new empty list
                }
                return retrieveWish; // returns list
            }
            
            var tempWish = loadList(); // create temp array to pull from storage
            
            function saveState() {
                localStorage.setItem("wishState", JSON.stringify(tempWish));
            }

            // adds product to server-side (online) wishlist
            function addServerItem(productName) {
                req=new XMLHttpRequest();
                req.onreadystatechange=function(){
                    if (this.readyState==4 & this.status==200) {
                        alert(this.response);
                    }
                };
                req.open("GET","addWishlistProduct.cgi?productName="+productName);
                req.send();
            }

            // adds product to client-side (offline) wishlist
            function addItem(productName) {
                if (loadList().includes(productName)) { // if list already contains item --> wont add
                    alert('Item already in list');
                } else { // pushes item to end of array
                    tempWish.push(productName);
        
                    saveState();
                    alert(productName + ' has been added offline');
                }
            }

            // removes product from server-side (online) wishlist
            function removeServerItem(productName) {
                req=new XMLHttpRequest();
                req.onreadystatechange=function(){
                    if (this.readyState==4 & this.status==200) {
                        alert(this.response);
                    }
                };
                req.open("GET","removeWishlistProduct.cgi?productName="+productName);
                req.send();
            }

            // removes product from client-side (offline) wishlist
            function removeItem(productName) {
                if (!(loadList().includes(productName))) { // if list already doesnt have item --> prompt nothing to remove
                    alert('Item was not in list to begin with!');
                } else { // find position of element and remove it
                    var pos = tempWish.indexOf(productName);
                    var removeProduct = tempWish.splice(pos, 1); // removes the found product from the list
        
                    saveState();
                    alert(productName + ' has been removed offline');
                }
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
    <h1>Product Listing Page</h1>
    <div class='productList'>
    </div>
"""

# ------ Generating Products from database
# Finds the original list of products with no owners
products = db.products.find({'owner':'null'})
for record in products: # Creates and displays relevant info for each product in catalogue
    print "<h3>"+record['name']+"</h3>"
    print "<a href='individualProductPage.cgi?productName="+record['name']+"'>Visit "+record['name']+" Product Page</a>"
    print "<br>"
    print "<button id='addButton_"+record['id']+"'>Add to wishlist</button>"
    print "<button id='removeButton_"+record['id']+"'>Remove from wishlist</button>"
    if statusName: # if signed in, remove products from server
        # Adding event listeners to add buttons via javascript
        print "<script>document.getElementById('addButton_"+record['id']+"').addEventListener('click',function(){addServerItem('"+record['name']+"');});</script>"
        # Adding event listeners to remove buttons via javascript
        print "<script>document.getElementById('removeButton_"+record['id']+"').addEventListener('click',function(){removeServerItem('"+record['name']+"');});</script>"
    else: # offline
    # Adding event listeners to add buttons via javascript
        print "<script>document.getElementById('addButton_"+record['id']+"').addEventListener('click',function(){addItem('"+record['name']+"');});</script>"
        print "<script>document.getElementById('removeButton_"+record['id']+"').addEventListener('click',function(){removeItem('"+record['name']+"');});</script>"
            
    print "<br>"
    print "<img class='overviewImage' src='"+record['image']+"'>""</img>"

# Bottom shared element
print open('pageDesign.bottom','r').read()
"""
    </body>
</html>
"""