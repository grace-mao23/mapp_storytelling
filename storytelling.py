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
  command("SELECT accounts.username FROM accounts WHERE accounts.username = \'{}\'".format(username))
  if len(c.fetchall()) > 0:
    #c# flash message here
    return "username exists"
  elif password != passwdverf:
    #c# flash message here
    return "password does not match"
  else:
    addRow("accounts", (username, password))
    return "account created"

#c# testing account creation    
#x# print (createAccount("d", "d", "d")) 
#x# print (createAccount("d", "d", "d")) #c# should say exists
#x# print (createAccount("doof", "d", "ddd")) #c# passes don't match
#x# print (createAccount("doof", "d", "d")) #c#  
  
db.close()  #close database
#c# Bottom of DB Code