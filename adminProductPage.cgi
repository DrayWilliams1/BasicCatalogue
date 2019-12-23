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

form = cgi.FieldStorage() # gets access to the submitted form data (only instantiate one)
product_id = form.getfirst('id') # gets product id from form
product_name = form.getfirst('name') # gets product name from form
product_description = form.getfirst('description') # gets product description from form
product_cost = form.getfirst('cost') # gets product cost from form

if product_id!=None and product_name!=None and product_description!=None and product_cost!=None: # if username and password were input
    product_id = str(product_id)
    product_name = str(product_name)
    product_description = str(product_description)
    product_cost = str(product_cost)

    # a default image and a null owner is assigned for the new product
    newProduct = {'id':product_id,'name':product_name,'description':product_description,'cost':product_cost,'image':'basicCar.png','owner':'null'}
    
    tempNewProductCheck = db.products.find_one({'id':product_id,'name':product_name})
    
    # checks database for pre-existence of new product
    if tempNewProductCheck==None: # similar product does not exist
        product=db.products.insert_one(newProduct) # add product to database
        print "<script>alert('Product added to database');</script>"
    else: # product already exists in database
        print "<script>alert('A product with that id/name already exists');</script>"
else: # missing one of the required fields
    print "<script>alert('The fields cannot be empty');</script>"

print """
<html>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <head>
        <title>Assignment 4 - Product Administration</title>
        <link rel="stylesheet" type="text/css" href="style.css">
        <script>
            // removes product database
            function removeFromDatabase(productName) {
                req=new XMLHttpRequest();
                req.onreadystatechange=function(){
                    if (this.readyState==4 & this.status==200) {
                        alert(this.response);
                    }
                };
                req.open("GET","removeDatabaseProduct.cgi?productName="+productName);
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
    <h1>Product Administration Page</h1>
    <p>Allowing users to view, add, or remove products from database</p>
    <div class='productList'>
    </div>

    <table cellpadding="5" cellspacing="10" align="left">
        <h3>Add Product to Database</h3>
        <form method="post">
            <tr><th>ID:</th><td><input type='text' name='id'/></td></tr>
            <tr><th>Name:</th><td><input type='text' name='name'/></td></tr>
            <tr><th>Description:</th><td><input type='text' name='description'/></td></tr>
            <tr><th>Cost:</th><td><input type='text' name='cost'/></td></tr>
            <tr><td colspan="2" align="right"><input type='submit' value='Add Product' name='login' /></td></tr>
        </form>
    </table>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <br>
    <h3>Current Database Products</h3>
    <p>View/Remove Products below</p>
"""
    
# ------ Generating Products from database
products = db.products.find({'owner':'null'})
for record in products: # Creates and displays relevant info for each product in catalogue
    print "<h4>"+record['name']+"</h4>"
    print "<a href='#'>Visit "+record['name']+" Product Page</a>"
    print "<br>"
    print "<button id='removeButton_"+record['id']+"'>Remove "+record['name']+" from database</button>"
    # Adding event listeners to remove buttons via javascript
    print "<script>document.getElementById('removeButton_"+record['id']+"').addEventListener('click',function(){removeFromDatabase('"+record['name']+"');});</script>"

# Bottom shared element
print open('pageDesign.bottom','r').read()
"""
    </body>
</html>
"""