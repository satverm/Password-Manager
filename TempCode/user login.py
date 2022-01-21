# This code is for crating a login page for the user
import hashlib as hs
import sqlite3 as sq
import random as rd

from pw_secure import ret_pw

def userlogin(userid = None, pwd= None):
    if userid == None:
        userid = input("Enter the userID: ")
    while True:
        if pwd == None:
            pwd = input("Enter the password: ")
            pwd_c = input("Enter the password again to confirm: ")
            if pwd == pwd_c:
                break
            else:
                print("The passwords entered by you don't match!! try again..")
    return([userid,pwd])
# The login test should be done after the user has entered a filename and the file is present and also having some data. The login test function will test if the password stored for the admin user(userID=1) is matching using the passphrase and the password provided by the user and allow login if result is True
def logintest(pwd = None, passphraase= None):
    while True:
        pass_phr = input("Enter the passphrase to login as admin: ")
        pass_phr_c = input("Enter the passphrase again to confirm: ")
        if pass_phr == pass_phr_c:
            break
        else:
            print("The passphrase entered by you don't match!! Try again..")
    # now hash the passphrase:
    # Now to login the admin we will first find the admin password using the ret_pw() function and entered hash
    # Then this password would be compared with password entered by the user and if they match then the user can login to UI.
    pwstored = ret_pw(None,1,pass_phr)
    while True:
        if pwd == None:
            pwd = input("Enter the admin password: ")
            pwd_c = input("Enter the password again to confirm: ")
            if pwd == pwd_c:
                break
            else:
                print("The passwords entered by you don't match!! try again..")
    #compare the stored password with user provided admin password:
    if pwstored == pwd:
        login_test = True
        print("You are logged in as admin!!")
    else:
        login_test = False
        print("The login details are not correct!!")
    return(login_test)