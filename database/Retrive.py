import mysql.connector
import os
from dotenv import load_dotenv
import base64 


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
        print("\nerror in GetUserId() in retrive.py: \n",str(e))

def RetriveInfo(email):
    db = ConnectDb()
    MyCursor = db.cursor()

    try:
        userId = GetUserId(email)
        table1=os.getenv("MYSQL_INVENTORY_TABLE")
        table2=os.getenv("MYSQL_LOGIN_TABLE")
        command = f'''
                SELECT
                {table1}.prod_id,
                {table1}.prod_name,
                {table1}.prod_price,
                {table1}.prod_qty,
                {table1}.prod_low_qty,
                {table1}.prod_category,
                {table1}.prod_size,
                {table1}.prod_weight,
                {table1}.prod_color,
                {table1}.supplier_name,
                {table1}.supplier_no,
                {table1}.prod_img,
                {table1}.prod_comments
                FROM {table1}
                INNER JOIN {table2} 
                ON {table1}.user_id = {table2}.Sno
                WHERE user_id= %s
                ORDER BY {table1}.prod_add_date desc;
                '''
        MyCursor.execute(command,(userId,))
        prodArr = MyCursor.fetchall()

        # ****************************************** new ************************************************
        if prodArr:
                formatted_products = []
                for product in prodArr:
                    img = product[-2]
                    encoded_img = base64.b64encode(img).decode("utf-8")
                    # formatted_products.append((product[0], product[1], encoded_img, product[2:]))
                    formatted_item = (*product[:-2], encoded_img, product[-1])
                    formatted_products.append(formatted_item)
                print("\n the formated array:")
        else:
            formatted_products = None

        # ****************************************** new ************************************************
        return formatted_products
        # return prodArr


    except Exception as e:
        print("\nerror in Retrive.py RetriveInfo() in getting the product info by user_id\n",str(e))
        prodArr = MyCursor.fetchwarnings()
        return prodArr
        

if __name__ == "__main__":
    a = RetriveInfo("lelopuvu@mailgolem.com")
    print(a)