#Team mapp - Junhee Lee, Kelvin Ng, Pratham Rawat
#SoftDev1 pd0
#Storytelling Site
#2019-10-28

import sqlite3



#b# Database Code ==========================================================


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

#c# testing
#x# comm("CREATE TABLE wry(testInt INTEGER)")
#x# commit()

#c# testing buildTable 
testChain = {"t1": "TEXT", "t2": "INTEGER", "t3":"INTEGER"}
#x# print (buildTable("HeWo", testChain))
buildTable("HeWo", testChain)

db.close()  #close database
#c# Bottom of DB Code