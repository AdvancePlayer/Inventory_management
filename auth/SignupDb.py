import mysql.connector
from dotenv import load_dotenv
import os
import bcrypt
load_dotenv()

def CreateDB():
    db = mysql.connector.connect(host = os.getenv("MYSQL_HOST"),password = os.getenv("MYSQL_PASSWORD"),user = os.getenv("MYSQL_USER"))
    MyCursor = db.cursor()
    command = "CREATE DATABASE IF NOT EXISTS {};".format(os.getenv("MYSQL_DATABASE"))
    MyCursor.execute(command)
    command = "USE DATABASE {};".format(os.getenv("MYSQL_DATABASE"))
    MyCursor.execute(command)
    command = "CREATE TABLE {}(Sno INT NOT NULL AUTO_INCREMENT PRIMARY KEY,email VARCHAR(30) NOT NULL,password VARCHAR(255) NOT NULL);".format(os.getenv("MYSQL_LOGIN_TABLE"))
    MyCursor.execute(command)
    db.close()

def SignUp(username,password):
    try:
        db = mysql.connector.connect(host = os.getenv("MYSQL_HOST"),user = os.getenv("MYSQL_USER"),password = os.getenv("MYSQL_PASSWORD"), database=os.getenv("MYSQL_DATABASE"))
        MyCursor = db.cursor()
        command = "SHOW TABLES LIKE '{}';".format(os.getenv("MYSQL_LOGIN_TABLE"))
        MyCursor.execute(command)
        if MyCursor.fetchone() != None:
            pass
        else:
            command = "CREATE TABLE IF NOT EXISTS {}(Sno int NOT NULL AUTO_INCREMENT PRIMARY KEY,email VARCHAR(30) NOT NULL,password VARCHAR(255) NOT NULL,account_created TIMESTAMP DEFAULT now(););".format(os.getenv("MYSQL_LOGIN_TABLE"))
            MyCursor.execute(command)
    except mysql.connector.Error as e:
        print(e)
        CreateDB() 
        print("\ndatabase was not present so new database created with table")
    except Exception as e:
        print("\nerror in login() in login.py:-\n"+e)

    command = "SELECT email FROM {} WHERE email = %s".format(os.getenv("MYSQL_LOGIN_TABLE"))
    MyCursor.execute(command,(username,))
    print(MyCursor.fetchone())
    if MyCursor.fetchone() != None:
        return False
    else:
        try:
            bytesn = password.encode("utf-8")
            salt = bcrypt.gensalt()
            HashPassword = bcrypt.hashpw(bytesn,salt)
        except:
            print("\n password cannot be hashed (error in SignUp() in SignUp.py)")
            return False

        command = "INSERT INTO {}(email,password) VALUES(%s,%s);".format(os.getenv("MYSQL_LOGIN_TABLE"))
        MyCursor.execute(command,(username,HashPassword))
        db.commit()
        print("\nuser Added : ",username,HashPassword)
    return True

if __name__=="__main__":
    p = SignUp("a","a")
    print(p)