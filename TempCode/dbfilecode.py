# This is the test code for database file check
import sqlite3 as sq

def dbfilecheck():
    file_present = False
    with open(dbfile,'r') as fr:
        file_present= True
    if file_present == False:
        print("The database file needs to be created!")
        print("Creating a new database file..")
        con = sq.connect(dbfile)
        con.close()
        print("Database file named {} has been created.".format(dbfile))
    else:
        return(file_present)
