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
print "Content-Type: text/html"
print

print """
<html>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <head>
        <title>Assignment 4 - Merge Loader</title>
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
            
            function saveState() {
                localStorage.setItem("wishState", JSON.stringify(tempWish));
            }


            function mergeLists() {
                var tempWish = loadList().filter(Boolean); // removes empty indices (if any)
                var concatProducts = "";
                tempWish.forEach(function(item, index) {
                    concatProducts = concatProducts.concat(item);
                    concatProducts = concatProducts.concat(",");
                    }
                );

                concatProducts = concatProducts.substring(0, concatProducts.length - 1);
                        
                req=new XMLHttpRequest();
                req.onreadystatechange=function(){
                    if (this.readyState==4 & this.status==200) {
                        alert(this.response); // will message what products were merged
                        
                        tempWish = [] // clears offline list and saves it to local storage
                        localStorage.setItem("wishState", JSON.stringify(tempWish));

                        window.location.replace('./productListingPage.cgi');
                    }
                };
                req.open("GET","mergeLists.cgi?productList="+concatProducts);
                req.send();
            }

            // When the page loads, make ajax request to merge lists
            window.addEventListener('load',
                function() {
                    mergeLists();
                }
            );
        </script>
    </head>
    <body>
"""
# Top shared element
print open('pageDesign.top','r').read()

print """
    Merging Lists...
"""
# Bottom shared element
print open('pageDesign.bottom','r').read()
"""
    </body>
</html>
"""