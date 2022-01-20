# Password-Manager ( User provided database file name)
# This repository is created using the pw-login branch of the Secure-Pass repo.
The project is for learning and is under development.
This will include codes related with storing usernames and passwords in a secure way.
The password is hashed by using a passphrase which the user has to remember and user can use the same passphrase to retrieve the password.
The secured password is stored in a sqlite3 database file in the same forlder where the program is present.
# Features:
 1. User can store passwords along with the username and the name of the website or service for which the password is required.
 2. The stored password can be updated or deleted from the database after it is stored.
 3. All the stored usernames servicenames and the ID used in the database can be viewed.
 4. The passwords can be retrieved in case you forgot or you want to confirm before using it for some task.
 
 
## Note: if you store a password with some range specified at the beginning of the code and then try to retrieve the password from a range which does not fall within the original range then the passwords can't be retrieved. If you don't remember the range, you can try with some big range say 100000 to 200000 to retrieve the passwords. Bigger numbers are defined so that it takes more time for some one else to retrieve the password provided he also knows the passphrase.

## Updates: 
Full terminal/Text based UI completed.
This branch is now designed to work with any file created by the user and not a default file. Thus now the user can use this program without the need of modifying the database file name in the program.
Thus, now the user can create as many files for different group of passwords as per his own choice.

## Smart Secure: Secure the password by making the lim_min and lim_max variable very large and a difference of atleast 10,000 between them (for example 800000 and 810000) and then revert the code to the default value of 1000 and 2000.
## To do: Moved to ToDo.org file.





