# This program is used to store and retrieve the password in a secured way by using a pass-phrase.
# The logic is to hash the pass-phrase and then generate the hashes for each character of the password using the pass-phrase hash.
# Various methods would be uesd to ensure that the stored hashes are all unique even if the password and the passphrase for any two userid/service are same.
# Random values are used not for security but to make the hashes look random and make if difficult to find the number of characters in the password.
# To retrieve the password, the pass-phrase is entered by the user and the characters of the password are recovered back by generating the
# hashes and comparing with the stored hashes.
# Sqlite3 database can be used to store the data in a file for persistance and use by other functions.

import hashlib as hs

import sqlite3 as sq

import random as rd


# dbfile= 'pw_wallet_1_01.db'  # The file name can be changed by the user here only to have different names.
# The difference between ran_min and ran_max can be made large to increase the time for retrieving the passworod and also
lim_min, lim_max = 1, 10
# to randomise the hashes so that they are different even for same password and passphrase pairs. The security is provided by the passphrase without which even with
# the data of hashes there is no way to find the passwords.
# These limits can also be used as a smart feature to store the passwords using some big value but a small range of say 1000 and use the
# same during retrieving process. So this can act as additional way of increasing diffuculty for others to retrieve the passwords.
# Adds random (1-10)number of fake hashes in the database.
fake_hash_limit = 1
#print("The program is used to store and retrieve passwords securely\n")

# secure_pw: will convert the password into random hashes list based on the passphrase provided by the user.
def secure_pw(user_name=None, service=None, passwd=None, pass_phrase=None, ran_min=None, ran_max=None):

    if user_name == None:
        user_name = input("Enter the username: ")

    if service == None:
        service = input("Enter the service name: ")

    if passwd == None:
        while True:
            passwd = input(
                "Enter the password to store for the given username and service: ")
            pwd_c = input("Enter the password again to confirm: ")

            if passwd == pwd_c:
                break
            else:
                print("The password do not match !! Try again..")

    if pass_phrase == None:
        while True:
            pass_phrase = input("Enter the passphrase: ")
            print("Write the pass phrase in a paper for future refrence.")
            pass_phrase1 = input("Enter the pass phrase again to confirm: ")

            if pass_phrase == pass_phrase1:
                break
            else:
                print("The pass phrase entered by you don't match !! Try again...")

    if ran_min == None:
        ran_min = lim_min

    if ran_max == None:
        ran_max = lim_max

    ps_phr_hsh = hs.sha256(pass_phrase.encode('utf-8')).hexdigest()
    pw_hsh_lst = []
    n_count = 0

    for char in passwd:
        n_count += 1
        # Add a random number string in the hash to randomize the hashes
        ran_num = rd.randint(ran_min, ran_max)
        temp_str = str(ran_num) + char + chr(n_count) + str(ps_phr_hsh)
        pw_ch_hsh = hs.sha256(temp_str.encode('utf-8')).hexdigest()
        pw_hsh_lst.append(pw_ch_hsh)

## testing fo less hashes
        test_hash_list = []
        print("The present pw_chr_hash is: ",pw_ch_hsh)
        print('The list for pw char:{}, ser: {}'.format(char,n_count))
        for char in range(128):
            for k in range(ran_min,ran_max):
                temp_str = str(k) + chr(char) + chr(n_count) + str(ps_phr_hsh)
                pw_ch_hsh_test = hs.sha256(temp_str.encode('utf-8')).hexdigest()
                test_hash_list.append(pw_ch_hsh_test)
        for item in sorted(test_hash_list):
            print(item)



    # Code to add random hashes, this can be converted into a function and be called as per requirement, this will enable the flexibility in the code
    ran_int = rd.randint(1, fake_hash_limit)

    for i in range(ran_int):
        temp_str1 = str(ps_phr_hsh) + str(rd.randint(10000, 100000))
        ran_hsh = hs.sha256(temp_str1.encode('utf-8')).hexdigest()
        pw_hsh_lst.append(ran_hsh)

    pw_record = [user_name, service, str(pw_hsh_lst)]
    # store_record(pw_record)
    print("The password has been secured and stored in database\n")

    return(pw_record)


# ret_pw: will retrieve the password using the same passphrase as used to secure and store.
def ret_pw(dbfile=None, sel_id=None, pass_phrase=None, ran_min=None, ran_max=None):
    print("The program will  retrieve the password by using the passphrase\n")

    if dbfile == None:
        dbfile = db_file_chk()

    if sel_id == None:
        sel_y = str(
            input("To see the database ID, UserName and Service name press Y/y:"))

        if sel_y.lower() == 'y':
            rec_lst = get_all_records(None, dbfile)

            for item in rec_lst:
                print("ID={}    | UserName={}      | Service= {}".format(
                    item[0], item[1], item[2]))

        sel_id = input("Enter the ID  to retrieve the password: ")

    # Now get the record from the database for the selected id and retrieve password using the passphrase
    if get_all_records(sel_id, dbfile) == []:
        print("The selected ID is not present!!")
    else:
        rec_list = sel_rec(sel_id, dbfile)
        pw_hash_list = rec_list[3]

        if pass_phrase == None:
            pass_phrase = input("Enter the pass phrase: ")

        ps_phr_hsh = hs.sha256(pass_phrase.encode('utf-8')).hexdigest()

        if ran_min == None:
            ran_min = lim_min

        if ran_max == None:
            ran_max = lim_max

        n_count = 0
        pword = ''

        for item in pw_hash_list:
            tmp_chk = False
            n_count += 1

            for i in range(128):
                tmp_chk = False

                for j in range(ran_min, ran_max+1):
                    temp_str = str(j) + chr(i) + chr(n_count) + str(ps_phr_hsh)
                    chk_hsh = hs.sha256(temp_str.encode('utf-8')).hexdigest()

                    if item[1:7] == chk_hsh[0:6]: ##Testing the option of storing only few hashes.
                    #if item[1:-1] == chk_hsh:
                        pword += chr(i)
                        #print("character{} is {}".format(n_count,chr(i)))
                        tmp_chk = True
                        break

                if tmp_chk == True:
                    break

            if pword == '':
                print("The pass phrase is incorrect !!")
                break
            else:

                if tmp_chk == False:
                    print("\nThe stored password is: '{}' ".format(pword))
                    break

        return(pword)


# Function for storing the secured password in a sqlite3 database file(filename.db) to be provided by the user.
def store_record(record=None, dbfile=None):

    if dbfile == None:
        dbfile = db_file_chk()

    if record == None:
        record = secure_pw()

    con = sq.connect(dbfile)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS pwTAB(userID integer primary key autoincrement not null, UserName text, Service text, pwHash text)''')
    cur.execute(
        'INSERT INTO pwTAB(UserName,Service,pwHash) VALUES(?,?,?)', record)
    con.commit()
    con.close()
    print("Password database updated in {}".format(dbfile))


# del_rec: function to delete a record from the database file based on the ID of the record.
def del_rec(sel_id=None, dbfile=None):

    if dbfile == None:
        dbfile = db_file_chk()

    if sel_id == None:
        print("The records stored in the database are: ")
        print_records(sel_id, dbfile)
        sel_id = (input("Enter the id for which record is to be deleted: "))
    else:
        rec_lst = get_all_records(sel_id, dbfile)

    if sel_rec == []:
        print("The selected ID is not present !!")
    else:
        print_records(sel_id, dbfile)
        con = sq.connect(dbfile)
        cur = con.cursor()
        cur.execute('DELETE FROM pwTAB WHERE userID = (?)', (sel_id,))
        con_del = input("Press Y/y to  confirm deleting the selected record: ")

        if con_del.lower() == 'y':
            con.commit()
            print("The selected id {} has been deleted!!".format(sel_id))
        else:
            print("The selected record has not been deleted.")

        con.close()


# update_rec: used to store a new password for some already stored record.
def update_rec(sel_id=None, dbfile=None):

    if dbfile == None:
        dbfile = db_file_chk()

    if sel_id == None:
        print("The records stored in the database are: ")
        print_records(sel_id, dbfile)
        sel_id = input("Enter the id for which password is to be updated: ")
    else:
        print("The selected record is as under: ")
        print_records(sel_id, dbfile)

    if get_all_records(sel_id, dbfile) == []:
        print("The entered ID is not present!!")
    else:
        rec_to_updt = sel_rec(sel_id, dbfile)
        updated_rec = secure_pw(rec_to_updt[1], rec_to_updt[2])
        con = sq.connect(dbfile)
        cur = con.cursor()
        cur.execute('UPDATE pwTAB  SET pwHASH = (?) WHERE userID = (?)',
                    (updated_rec[2], sel_id,))
        con_updt = input(
            "Press Y/y to  confirm updating the selected record: ")

        if con_updt.lower() == 'y':
            con.commit()
            print("The selected id {} has been updated!! in {} .".format(
                sel_id, dbfile))
        else:
            print(
                "The selected record has not been updated in database file: {}".format(dbfile))

        con.close()


# sel_rec: used to select the record and the hashlist in the required format.
def sel_rec(sel_id=None, dbfile=None):
    if dbfile == None:
        dbfile = db_file_chk()

    if sel_id == None:
        sel_id = input("Enter the id  to select the record: ")

    if get_all_records(sel_id, dbfile) == []:
        print("The entered ID is not present!!")
        rec_list = []
    else:
        con = sq.connect(dbfile)
        cur = con.cursor()
        cur.execute('SELECT * FROM pwTAB WHERE userID = (?)', (sel_id,))
        record = cur.fetchone()
        con.close()
        tmp_str = str(record[3])
        tmp_str1 = tmp_str.strip("[]")
        hash_list = tmp_str1.split(', ')
        rec_list = [record[0], record[1], record[2], hash_list]
        # print(rec_list)

    return(rec_list)


# get_all_records: used to get a list of all or one record from the database except the hashlist.
def get_all_records(sel_id=None, dbfile=None):
    if dbfile == None:
        dbfile = db_file_chk()

    con = sq.connect(dbfile)
    cur = con.cursor()

    if sel_id != None:
        #sel_id = input("Enter the id  to select the record: ")
        cur.execute('SELECT * FROM pwTAB WHERE userID = (?)', (sel_id,))
        record = cur.fetchall()
    else:
        cur.execute('SELECT * FROM pwTAB')
        record = cur.fetchall()

    con.close()

    return(record)


# print_records: print all or one record from database.
def print_records(sel_id=None, db_file=None):
    rec_lst = get_all_records(sel_id, db_file)

    for item in rec_lst:
        print("ID={}    | UserName={}      | Service= {}".format(
            item[0], item[1], item[2]))


# Muitiple entries
def multi_entries(dbfile = None):
    if dbfile is None:
        dbfile = db_file_chk()
    while True:
        record = secure_pw()
        store_record(record,dbfile)
        print("The password has been stored!")
        sel_next = input("Enter Y/y to add more passwords or Enter to exit: ")
        if sel_next.lower() != 'y':
            break



# db_create: used to create a new database file when running for first time anytime if the user wants.
def db_create(db_file=None):
    while True:
        if db_file == None:
            db_file = str(
                input("Enter the new database file name to create(anyfilename.db): "))

        if db_file_chk(db_file) != False:
            print("The entered file already exists!!\nChose a different name.")
            db_file = None
        else:
            if db_file[-3:] != '.db':
                print("The filename extension should be .db !!, try again!!")
                db_file = None
            else:
                break

    print("The first record in the database will be used for user login.\n")
    user = input("Enter the admin name for managing the passwords: ")

    while True:
        ad_pw = input("Enter the admin password: ")
        ad_pwc = input("Enter the password again to confirm: ")

        if ad_pw != ad_pwc:
            print("The passwords entered by you don't match!! enter again..")
        else:
            break

    while True:
        ad_ps_phr = input("Enter the admin passphrase: ")
        print("### NOTE THE PASSPHRASE IN SOME PAPER AS IT WILL BE USED TO RETRIEVE ANY PASSWORD ###")
        ad_phrc = input("Enter the passphrase again to confirm: ")

        if ad_ps_phr != ad_phrc:
            print("The passphrase entered by you don't match!! enter again..")
        else:
            break

    con = sq.connect(db_file)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS pwTAB(userID integer primary key autoincrement not null, UserName text, Service text, pwHash text)''')

    store_record(secure_pw(user, 'administration', ad_pw, ad_ps_phr), db_file)

    con.commit()
    con.close()

    print("Following admin user has been created, the same would be used for managing the data.")
    print_records(None, db_file)
    print("The database file {} has been created!!".format(db_file))

    return(db_file)


# db_file_chk: check if the entered file is present and return the filename if present or False if not present in the program dir.
def db_file_chk(db_file=None):
    if db_file == None:
        db_file = str(
            input("Enter the filename to access you data (filename.db): "))
        #print("The file selected by you is:",db_file)

    try:
        with open(db_file, 'r') as fr:
            #print("file is present")
            return(db_file)

    except IOError:
        #print("The entered file is not present in the program directory!!")
        #print("Ensure the file is present in the program directory")
        # todo: code to tell user exit and to copy datafile in the program folder or enter the correct file name

        return(False)


# The login test should be done after the user has entered a filename and the file is present and also having some data. The login test function will test if the password stored for the admin user(userID=1) is matching using the passphrase and the password provided by the user and allow login if result is True
def logintest(db_file=None, pass_phr=None, pwd=None):
    if db_file == None:
        db_file = input(
            "Enter the stored database file name(youfilename.db): ")
        test_file = db_file_chk(db_file)

    if test_file != False:
        while True:
            if pass_phr == None:
                pass_phr = input("\nEnter the passphrase to login as admin: ")
                pass_phr_c = input("Enter the passphrase again to confirm: ")

                if pass_phr == pass_phr_c:
                    break
                else:
                    pass_phr = None
                    print("\nThe passphrase entered by you don't match!! Try again..")

        while True:
            if pwd == None:
                pwd = input("\nEnter the admin password: ")
                pwd_c = input("Enter the password again to confirm: ")

                if pwd == pwd_c:
                    break
                else:
                    pwd = None
                    print("\nThe passwords entered by you don't match!! try again..")

        # Now to login the admin we will first find the admin password using the ret_pw() function and entered hash
        # Then this password would be compared with password entered by the user and if they match then the user can login to UI.
        # compare the stored password with user provided admin password:
        pw_stored = ret_pw(db_file, '1', pass_phr)

        if pw_stored == pwd:
            login_test = True
            print("\n***You are logged in as admin!!***")
        else:
            login_test = False
            print("\nThe login details are not correct!!")

        return([login_test, db_file])

    else:
        print("\nThe file name entered by you is not present!!")

        return([test_file, test_file])


# pw_ui: The user interface for all tasks of the program.
def pw_ui():
    # todo: prompt user if he is new or wants to create a new file.
    # todo: test for the fileanme to have .db extension
    print("\n*** The program is used for storing and retrieving your password ***")
    print("\nNew user needs to create a database file and login details!!")

    test_user = input(
        ("\nPress Y/y if you have already created a database file or Enter to create a new user: "))

    if test_user.lower() == 'y':
        print("\n\n*** User Login ***")
        # test if the database file is present and login details match with data in file.
        login_chk = logintest()

        if login_chk[0] == True:
            # set dbfile to the filename entered by user if login test passes.
            dbfile = login_chk[1]
        else:
            #print("The filename entered by you is not present in the program direcotory")
            dbfile = False

    else:
        dbfile = False

    #file_nam= str(input("Enter the database file name (filename.db):"))
    #dbfile = db_file_chk(file_nam)
    nofile = False

    if dbfile == False:
        nofile = True
        new_file_opt = str(
            input("\nPress Y/y to create a new file or any other key to exit!!: "))

        if new_file_opt.lower() == 'y':
            print("\n*** New user and database file***")
            dbfile = db_create()

            if db_file_chk(dbfile) == False:
                nofile = True
            else:
                nofile = False

        else:
            nofile = True

    if not nofile:
        task_list = ["0: Exit", "1: Store new Password", "2: Update password",
                     "3: Delete Password Record", "4: Retrieve Password", "5: View Usernames ID", "6: Multiple Entries"]
        print("\nFollowing tasks can be performed:-\n")

        for item in task_list:
            print(item)  # print(task_list)

    while not nofile:
        sel_task = str(input("\nEnter the number for the Selected Task: "))

        if sel_task == '1':
            store_record(None, dbfile)

        elif sel_task == '2':
            update_rec(None, dbfile)

        elif sel_task == '3':
            print("\nThe program will DELETE record from database!!")
            del_rec(None, dbfile)

        elif sel_task == '4':
            ret_pw(dbfile)  # todo: avoid double printing of selected record

        elif sel_task == '5':
            print("\nRecords stored in the database : ")
            rec_list = get_all_records(None, dbfile)

            if rec_list == []:
                print("There are no records in the database at present!!")
            else:
                print_records(None, dbfile)
        elif sel_task == '6':
            print("Add multiple entries:")
            multi_entries(dbfile)

        elif sel_task == '0':
            #print("The program completed!!")
            break

        else:
            print("No valid input recieved !!")

        task_opt = input(
            "\nPress Y or y to get the task list again or any other key to Exit : ")

        if task_opt.lower() == 'y':

            for item in task_list:
                print(item)

        else:
            break

    print("The program completed!!")


# main: The entry point for the program.
def main():
    secure_pw('sat','serv','a','pass')
    #pw_ui()


# code string to start main()
if __name__ == "__main__":
    main()
