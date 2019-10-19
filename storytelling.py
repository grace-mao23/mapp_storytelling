#Team mapp - Junhee Lee, Kelvin Ng, Pratham Rawat
#SoftDev1 pd0
#Storytelling Site
#2019-10-28

import sqlite3

#b# ========================================================================

#b# Database Interaction ===================================================
db = sqlite3.connect("mapp_site.db") #open if file exists, otherwise create
c = db.cursor()

#d# save changes  
def commit():  
  db.commit()
  
#d# calls c.execute(command)
def command(command):
  c.execute(command)

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

#b# Accounts Table Code ====================================================

buildTable("accounts", {"username": "TEXT", "password": "TEXT"})

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

def loginAccount(username, password):
  command("SELECT username, password FROM accounts WHERE username = \'{}\'".format(username))
  fetched = c.fetchall()
  if len(fetched) < 1:
    #c# flash message here
    return "username does not exist"
  elif fetched[0][0] != password:
    #c# flash message here
    return "password is incorrect"
  else:
    #c# cache login here
    return "login successful"
    
#c# testing account creation    
#x# print (createAccount("d", "d", "d")) 
#x# print (createAccount("d", "d", "d")) #c# should say exists
#x# print (createAccount("doof", "d", "ddd")) #c# passes don't match
#x# print (createAccount("doof", "d", "d")) #c#  

#c# testing account login
#x# print (loginAccount("dododd","D")) #c# bad user 
#x# print (loginAccount("d","D")) #c# bad pass
#x# print (loginAccount("d","d"))

db.close()  #close database
#c# Bottom of DB Code