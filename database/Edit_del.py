import mysql.connector
import os
from dotenv import load_dotenv


def ConnectDb():
    try:
        db = mysql.connector.connect(host = os.getenv("MYSQL_HOST"),user = os.getenv("MYSQL_USER"),password = os.getenv("MYSQL_PASSWORD"), database=os.getenv("MYSQL_DATABASE"))
        return db
    except Exception as e:
        try:
            db = mysql.connector.connect(host = os.getenv("MYSQL_HOST"),user = os.getenv("MYSQL_USER"),password = os.getenv("MYSQL_PASSWORD"))
            command = "USE {}".format(os.getenv("MYSQL_DATABASE"))
            db.cursor().execute(command)
            return db
        except:
            print("\ndb cannot be connected in AddProd.py: \n",str(e))
            return False


def GetUserId(email):
    db = ConnectDb()
    MyCursor = db.cursor()

    try:
        command = "SELECT Sno FROM {} WHERE email = %s;".format(os.getenv("MYSQL_LOGIN_TABLE"))
        MyCursor.execute(command, (email,))
        userId = MyCursor.fetchone()
        print("user id of :",email,"is = ",userId[0])
        return userId[0]
    except Exception as e:
        print("\nerror in GetUserId() in Edit_del.py: \n",str(e))

def DeleteProd(email,prod_id):
    db = ConnectDb()
    MyCursor = db.cursor()

    try:
        userId = GetUserId(email)
        command = '''
                DELETE FROM {} WHERE prod_id = %s AND user_id = %s;
                '''.format(os.getenv("MYSQL_INVENTORY_TABLE"))
        MyCursor.execute(command,(prod_id,userId))
        del_prod_resp = MyCursor.fetchwarnings()
        db.commit()
        if del_prod_resp:
            print("there is error in deletion",del_prod_resp)
            del_prod_resp = "The product cannot be deleted"
        else:
            print("the deletion is done in db (warnings):-\n",del_prod_resp)
            del_prod_resp = "Product is deleted successfully"
        # return del_prod_resp
    except Exception as e:
        print("\nerror in Edit_del.py DeleteProd() in getting the product info by user_id\n",str(e))
        del_prod_resp = "The product cannot be deleted"
        # return del_prod_resp
    

if __name__ == "__main__":
    DeleteProd("lelopuvu@mailgolem.com","ba001")