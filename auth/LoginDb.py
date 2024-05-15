import mysql.connector
import os
import bcrypt
from dotenv import load_dotenv


def Login(username, password):
    try:
        db = mysql.connector.connect(host=os.getenv("MYSQL_HOST"), user=os.getenv("MYSQL_USER"), password=os.getenv("MYSQL_PASSWORD"))
        MyCursor = db.cursor()
        command = "USE {};".format(os.getenv("MYSQL_DATABASE"))
        MyCursor.execute(command)
    except mysql.connector.Error as err:
        print("\nError connecting to MySQL in Login() at LoginDb.py: {}".format(err))
        return False

    try:
        command = "SELECT password FROM {} WHERE email = %s;".format(os.getenv("MYSQL_LOGIN_TABLE"))
        MyCursor.execute(command, (username,))
        HashPassword = MyCursor.fetchone()
        if HashPassword is not None:
            test = password.encode('utf-8') 
            result = bcrypt.checkpw(test, HashPassword[0].encode('utf-8'))
            return result
        else:
            return False
    except mysql.connector.Error as err:
        print("\nMySQL error in Login() at LoginDb.py: {}".format(err))
        return False
    finally:
        db.close()

if __name__ == "__main__":
    p = Login("aelopuv@mailgolem.com", "p")
    print(p)