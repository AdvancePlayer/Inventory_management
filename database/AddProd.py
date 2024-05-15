import mysql.connector
from dotenv import load_dotenv
import os


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

def AddProd(**prodinfo):
    db = ConnectDb()
    mycursor = db.cursor()
    print("db is connected ",db)

    try:
        command = '''CREATE TABLE IF NOT EXISTS {}(
                    prod_id VARCHAR(25),
                    prod_name VARCHAR(250) NOT NULL,
                    prod_price INT NOT NULL,
                    prod_qty INT NOT NULL,
                    prod_low_qty INT,
                    prod_category VARCHAR(20) NOT NULL,
                    prod_size VARCHAR(80),
                    prod_weight VARCHAR(80),
                    prod_color VARCHAR(100),
                    supplier_name VARCHAR(100) NOT NULL,
                    supplier_no BIGINT,
                    prod_img LONGBLOB,
                    prod_comments VARCHAR(266),
                    user_id INT NOT NULL,
                    prod_add_date TIMESTAMP DEFAULT now(),
                    foreign key(user_id) references login_details(Sno)
                    on delete cascade
                    on update cascade
                    );'''.format(os.getenv("MYSQL_INVENTORY_TABLE"))
        mycursor.execute(command)
        print("table is done !!")
        print("user id = ",prodinfo["userid"])
        print("product id = ",prodinfo["prod_id"])
        command = "SELECT prod_id FROM inventory WHERE user_id = %s AND prod_id = %s;"
        mycursor.execute(command,(prodinfo["userid"],prodinfo["prod_id"]))
        if mycursor.fetchall():
            return "Unsuccessful! Product cannot be added same with id: ",prodinfo["prod_id"]
        # microsrvices,and microservices in js
        else:
            command = '''INSERT INTO {} (prod_id,prod_name,prod_price,prod_qty,prod_low_qty,prod_category,prod_size,prod_weight,prod_color,supplier_name,supplier_no,prod_img,prod_comments,user_id)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''.format(os.getenv("MYSQL_INVENTORY_TABLE"))
            values = (prodinfo["prod_id"],prodinfo["prod_name"], prodinfo["prod_price"], prodinfo["prod_qty"],prodinfo["prod_low_qty"] , prodinfo["prod_category"],prodinfo["prod_size"] ,prodinfo["prod_weight"],prodinfo["prod_color"], prodinfo["supplier_name"], prodinfo["supplier_no"], prodinfo["prod_img"],prodinfo["prod_comments"] , prodinfo["userid"])
            mycursor.execute(command,values)
        print("Warnings in adding prod:",mycursor.fetchwarnings())
        db.commit()
        print("\nwarnings in addprod(): ",mycursor.fetchwarnings())
        print("\ndone adding the info")
        return "Successful! Product added with id: ",prodinfo["prod_id"]
    except Exception as e:
        print("\nInfo cannot be added in db error in AddProd():-\n",e)
        return "Unsuccessful! Product cannot be added with id: ",prodinfo["prod_id"]


if __name__ == "__main__":
    a = AddProd(prod_id="sk4d",prod_name = 'Product A',prod_price=100,prod_qty=50,prod_low_qty=5,prod_category='Electronics',prod_size="12X15X45",prod_weight=12,prod_color="red,blue,green",supplier_name='Supplier X',supplier_no=9458751254,prod_img=b'binary_image_data_here',prod_comments="No Comments",userid=1)
    print(a)