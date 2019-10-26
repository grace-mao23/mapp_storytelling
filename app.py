#Team mapp - Pratham Rawat, Junhee Lee, Kelvin Ng & David Xiedeng
#SoftDev1 pd1
# P#00 - Da Art of Storytellin'
# 2019-10-28

from flask import Flask, render_template, session, flash, request, redirect
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
        print("username in session")
        flash("Hello " + session['username'] + "!")
        return render_template('homepage.html') #user is redirected to the response page if logged in
    print("username not in session, redirecting to login")
    return redirect('/login') #returns to login page if user is not logged in

#d# two post inputs username and password
#d# returns to itself and flashes errors if bad login
#d# goes to homepage with successful login
@app.route("/login", methods=['GET', "POST"])
def login():
    #x# print (request)
    #x# print (request.form)
    #c# use .form when method is post
    #x# print (request.method)
    loginCode = ""
    try:
        loginCode = loginAccount(request.form["username"], request.form["password"])
    except:
        print("yeet")
	#c# bad login
	#x# print (loginCode)
    flash(loginCode)
	#x# render_template('homepage.html') #redirects to homepage if good login
    if loginCode == "Successful login":
        flash("Hello " + session['username'] + "!")
        return redirect('/')
    return render_template('login.html') #returns to login page if user is not logged in

@app.route("/logout")
def loggingOut():
    session.pop('username')		#removes session when logging out
    flash("You have successfully logged out!")
    return redirect("/")	#redircts to login page

@app.route("/create", methods=['GET', 'POST'])
def signUp():
    signUpCode = ""
    try:
        signUpCode = createAccount(request.form["username"], request.form["password"], request.form["password2"])
    except:
        print("yeet")
    flash(signUpCode)
    return render_template("createAccount.html")

@app.route("/createStory", methods=['GET', 'POST'])
def newStory():
	createStoryCode = ""
	#c# takes in inputs and moves to database
    #c# so far only title and story
	if request.method == 'POST':
		Title, Story = request.form['title'], request.form['introduction']
		createStoryCode = uploadStory(Title, Story)
		#c# returns here if error occurs
		if createStoryCode != "Story uploaded":
			flash(createStoryCode)
			#c# keeps input text if error pops up
			return render_template("createStory.html", ttle = Title, Story = Story)
		#c# moves to story page
		else:
			return render_template("homepage.html")
	#c# first time on page
	else:
		#c# may change to return to Story page
		return render_template("createStory.html", ttle = "", Story = "")

#b# Site Interaction
#b# ========================================================================
#b# Database Interaction

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
buildTable("stories", {"title": "TEXT", "story": "TEXT"})

#d# takes in three strings and reads from table accounts if data exists
#d# creates account if suitable input is provided
#d# returns String message
def createAccount(username, password, passwdverf):
    db = sqlite3.connect("mapp_site.db")
    c = db.cursor()
    c.execute("SELECT username FROM accounts WHERE username = \'{}\'".format(username))
    fetched = c.fetchall()
    db.close()
    if len(username) < 1:
        return "username too short"
    elif "'" in username:
        return "Please do not include ' in the username"
    elif len(password) < 1:
        return "password too short"
    elif len(fetched) > 0:
        #c# flash message here
        return "username exists"
    elif password != passwdverf:
        #c# flash message here
        return "password does not match"
    else:
        addRow("accounts", (username, password))
        return "account created"

def loginAccount(username, password):
    db = sqlite3.connect("mapp_site.db")
    c = db.cursor()
    cmd = "SELECT username, password FROM accounts WHERE username = '{}';".format(username)
    c.execute(cmd)
    fetched = c.fetchall()
    db.close()
    if len(fetched) < 1:
        return "username does not exist"
    elif fetched[0][1] != password:
        return "password is incorrect"
    else:
        session['username'] = username  #starts a session if user inputs correct existing username and password
        print('created session')
        #x# flash("Hello " + session['username'] + "! You have successfully logged in.")
        return "Successful login"

#d# pushes story inputs to database
#d# rejects upload if:
#d# - title is empty 
#d# - story is empty
#d# - title already exists 
def uploadStory(title, story):
	db = sqlite3.connect("mapp_site.db")
	c = db.cursor()
	c.execute("SELECT title FROM stories WHERE title = \'{}\'".format(title))
	fetched = c.fetchall()
	db.close()
	#c# title already exists
	#x# print(fetched)
	if len(fetched) > 0:
		return "Title already exists."
	#c# title is empty
	elif len(title) < 1:
		return "Please title your story"
	#c# story is empty
	elif len(story) < 1:
		return "Please write a story"
	else:
		addRow("stories", (title, story))
		return "Story uploaded"
    
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

#c# testing uploadStory
#x# print (uploadStory("", "pan-paka-paan")) #c# should say to title
#x# print (uploadStory("Atago", "")) #c# should say to write story
#x# print (uploadStory("Atago", "pan-paka-paan")) #c# should create story
#x# print (uploadStory("Atago", "Doun")) #c# should say title exists

#b# Accounts Table Code
#b# ========================================================================

db.close()  #close database
#c# Bottom of DB Code

if __name__ == "__main__":
    app.debug = True
    app.run()
