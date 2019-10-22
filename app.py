#Team mapp - Pratham Rawat, Junhee Lee, Kelvin Ng & David Xiedeng
#SoftDev1 pd1
# P#00 - Da Art of Storytellin'
# 2019-10-28

from flask import Flask, render_template, session, flash, request
import sqlite3, os

app = Flask(__name__)

db = sqlite3.connect("mapp_site.db") #open if file exists, otherwise create
c = db.cursor()

app.secret_key = os.urandom(32)
#b# ========================================================================
#b# Site Interaction

@app.route("/")
def loggingIn():
    if 'username' in session:
        flash("Hello " + session['username'] + "!")
        return render_template('homepage.html') #user is redirected to the response page if logged in
    return render_template('login.html') #returns to login page if user is not logged in

#d# two post inputs username and password
#d# returns to itself and flashes errors if bad login
#d# goes to homepage with successful login
@app.route("/login", methods=["POST"])
def login():
    #x# print (request)
    #x# print (request.form)
    #c# use .form when method is post
    #x# print (request.method)
	#x# print (request.form["username"], request.form["password"])
	user = request.form["username"]
	passw = request.form["password"]
	print (type(user), type(passw))
	#x# 
	loginCode = loginAccount(user, passw)
	#c# bad login
	#x# 
	print (loginCode)
	return render_template('login.html') #returns to login page if user is not logged in

#b# Site Interaction
#b# ========================================================================
#b# Database Interaction 

def openDB():
	db = sqlite3.connect("mapp_site.db") #open if file exists, otherwise create
	c = db.cursor()

def closeDB():
	db.close()
	
#d# save changes
def commit():
    db.commit()

#d# calls c.execute(command)
def command(command):
	db = sqlite3.connect("mapp_site.db") #open if file exists, otherwise create
	c = db.cursor()
	c.execute(command)
	db.commit()
	db.close()

#d# create table and remove table if exists
#d# takes in a filename and the key(dict)
def buildTable(name, kc):
    toBuild = "CREATE TABLE if not exists " + name + "("
    for el in kc:
        toBuild = toBuild + "{} {}, ".format(el, kc[el])
    toBuild = toBuild[:-2] + ")"
    command(toBuild)
    commit()

#d# adds data to table, whole row insertion
#d# takes string table, and list val
def addRow(table, val):
    toDo = "INSERT INTO {} VALUES (".format(table)
    for el in val:
        if type(el) == int:
            toDo = toDo + str(el) + ", "
        else:
            toDo = toDo + "\'" + el + "\'" + ", "
    toDo = toDo[:-2] + ")"
    command(toDo)
    commit()

#c# testing
#x# comm("CREATE TABLE wry(testInt INTEGER)")
#x# commit()

#c# testing buildTable
#x# testCols = {"t1": "TEXT", "t2": "INTEGER", "t3":"INTEGER"}
#x# print (buildTable("HeWo", testCols))
#x# buildTable("HeWo", testCols)

#c# testing addRow
#x# testRow = ("UwU", 10, 24)
#x# addRow("HeWo", testRow)

#b# Database Interaction
#b# ========================================================================
#b# Accounts Table Code

buildTable("accounts", {"username": "TEXT", "password": "TEXT"})

@app.route("/create")
#d# takes in three strings and reads from table accounts
def createAccount(username, password, passwdverf):
    
	command("SELECT username FROM accounts WHERE username = \'{}\'".format(username))
	
	if len(c.fetchall()) > 0:
        #c# flash message here
		return "username exists"
	elif password != passwdverf:
        #c# flash message here
		return "password does not match"
	else:
		addRow("accounts", (username, password))
		return "account created"

#d# takes in two strings and verifies presence in database
#d# returns int: 0 (bad user), 1 (bad pass), or 2 (success)
def loginAccount(username, password):
	db = sqlite3.connect("mapp_site.db")
	c = db.cursor()
	c.execute("SELECT username, password FROM accounts WHERE username = \'{}\'".format(username))
	fetched = c.fetchall()
	db.close()
	if len(fetched) < 1:
        #c# flash message here
		#c# "username does not exist"
		return 0
	elif fetched[0][0] != password:
        #c# flash message here
		#x# "password is incorrect"
		return 1
	else:
        #x# session['username'] = username  #starts a session if user inputs correct existing username and password
        #x# flash("Hello " + session['username'] + "! You have successfully logged in.")
		#x# render_template('homepage.html')     #redirects to homepage
		return 2

@app.route("/logout")
def loggingOut():
    session.pop('username')		#removes session when logging out
    flash("You have successfully logged out!")
    return redirect("/")	#redircts to login page

#c# testing account creation
#x# print (createAccount("d", "d", "d"))
#x# print (createAccount("d", "d", "d")) #c# should say exists
#x# print (createAccount("doof", "d", "ddd")) #c# passes don't match
#x# print (createAccount("doof", "d", "d")) #c#

#c# testing account login
#x# print (loginAccount("dododd","D")) #c# bad user
#x# print (loginAccount("d","D")) #c# bad pass
#x# 
#x# print (loginAccount("d","d"))

#b# Accounts Table Code
#b# ========================================================================

db.close()  #close database
#c# Bottom of DB Code

if __name__ == "__main__":
    app.debug = True
    app.run()
