#Team mapp - Junhee Lee, Kelvin Ng, Pratham Rawat
#SoftDev1 pd0
#Storytelling Site
#2019-10-28

import sqlite3



#b# Database Code ==========================================================

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
testCols = {"t1": "TEXT", "t2": "INTEGER", "t3":"INTEGER"}
#x# print (buildTable("HeWo", testCols))
buildTable("HeWo", testCols)

#c# testing addRow
testRow = ("UwU", 10, 24)
addRow("HeWo", testRow)

db.close()  #close database
#c# Bottom of DB Code