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
        # print("user id of :",email,"is = ",userId[0])
        return userId[0]
    except Exception as e:
        print("\nerror in GetUserId() in retrive.py: \n",str(e))



def ProductsInfo(email):
    db = ConnectDb()
    MyCursor = db.cursor()

    try:
        userId = GetUserId(email)
        table1=os.getenv("MYSQL_INVENTORY_TABLE")
        table2=os.getenv("MYSQL_LOGIN_TABLE")

        command = f'''
                SELECT COUNT(*) AS low_stock_count
                FROM {table1}
                INNER JOIN {table2} ON {table1}.user_id = {table2}.Sno
                WHERE user_id = %s
                AND {table1}.prod_qty <= {table1}.prod_low_qty;
                '''
        
        MyCursor.execute(command,(userId,))
        low_stock = MyCursor.fetchone()
        # print("Low stock:",low_stock[0])


        command = f'''
                SELECT COUNT(DISTINCT prod_category) AS total_categories
                FROM {table1}
                INNER JOIN {table2} ON {table1}.user_id = {table2}.Sno
                WHERE user_id = %s;
                '''
        MyCursor.execute(command,(userId,))
        categories = MyCursor.fetchone()
        # print("total categories(different):",categories[0])


        command = f'''
                SELECT COUNT(prod_id) AS total_products
                FROM {table1}
                INNER JOIN {table2} ON {table1}.user_id = {table2}.Sno
                WHERE user_id = %s;
                '''
        MyCursor.execute(command,(userId,))
        Total_Products = MyCursor.fetchone()
        # print("total products:",Total_Products[0])


        command = f'''
                SELECT COUNT(*) AS out_of_stock
                FROM {table1}
                INNER JOIN {table2} ON {table1}.user_id = {table2}.Sno
                WHERE user_id = %s
                AND
                {table1}.prod_qty = 0;
                '''
        MyCursor.execute(command,(userId,))
        out_of_stock = MyCursor.fetchone()
        # print("Out of stock:",out_of_stock[0])


        command = f'''
                SELECT COUNT(DISTINCT supplier_name) AS total_supplier
                FROM {table1}
                INNER JOIN {table2} ON {table1}.user_id = {table2}.Sno
                WHERE user_id = %s;
                '''
        MyCursor.execute(command,(userId,))
        Total_supplier = MyCursor.fetchone()
        # print("Total supplier(different):",Total_supplier[0])

        Prod_info = [low_stock[0],categories[0],Total_Products[0],out_of_stock[0],Total_supplier[0]]
        return Prod_info

    except Exception as e:
        print("\nInfo cannot be rertived from db error in DashboardInfo.py in ProductsInfo():-\n",str(e))
        Prod_info = ["N/A","N/A","N/A","N/A","N/A"]
        return Prod_info


def LowStockedInfo(email):
    db = ConnectDb()
    MyCursor = db.cursor()

    try:
        userId = GetUserId(email)
        table1=os.getenv("MYSQL_INVENTORY_TABLE")
        table2=os.getenv("MYSQL_LOGIN_TABLE")
        
        
        command = f'''
                SELECT {table1}.prod_img,
                {table1}.prod_name,
                {table1}.prod_qty,
                {table1}.prod_id
                FROM {table1}
                INNER JOIN {table2} ON {table1}.user_id = {table2}.Sno
                WHERE user_id = %s
                AND {table1}.prod_qty <= {table1}.prod_low_qty;

                '''
        MyCursor.execute(command,(userId,))
        low_stock_info = MyCursor.fetchall()
        # ****************************************** new ************************************************
        if low_stock_info:
                formatted_products = []
                for product in low_stock_info:
                    img = product[0]
                    encoded_img = base64.b64encode(img).decode("utf-8")
                    formatted_item = (encoded_img, *product[1:-1])
                    formatted_products.append(formatted_item)
                print("\n the formated array:",formatted_products[-1])
        else:
            formatted_products = None

        return formatted_products

        # ****************************************** new ************************************************
        # print("Low stock info:",low_stock_info)
        # return low_stock_info
    

    except Exception as e:
        print("\nInfo cannot be rertived from db error in DashboardInfo.py in LowStockedInfo():-\n",str(e))
        low_stock_info = ["N/A"]
        return low_stock_info


def LatestAdded(email):
    db = ConnectDb()
    MyCursor = db.cursor()

    try:
        userId = GetUserId(email)
        table1=os.getenv("MYSQL_INVENTORY_TABLE")
        table2=os.getenv("MYSQL_LOGIN_TABLE")

        limit = 8
        command = f'''
                    SELECT
                        {table1}.prod_id,
                        {table1}.prod_name,
                        {table1}.prod_price,
                        {table1}.prod_qty,
                        {table1}.prod_category,
                        {table1}.supplier_name,
                        {table1}.supplier_no,
                        {table1}.prod_img,
                        {table1}.prod_add_date
                    FROM {table1}
                    INNER JOIN {table2} ON {table1}.user_id = {table2}.Sno
                    WHERE user_id = %s
                    ORDER BY {table1}.prod_add_date DESC
                    LIMIT %s;
                '''
        MyCursor.execute(command,(userId,limit))
        Latest_added = MyCursor.fetchall()
        # print("Latest added info:",Latest_added)
        return Latest_added
    except Exception as e:
        print("\nInfo cannot be rertived from db error in DashboardInfo.py in LatestAdded():-\n",str(e))
        Latest_added = ["N/A"]
        return Latest_added


def SummaryInfoMonth(email):
    db = ConnectDb()
    MyCursor = db.cursor()

    try:
        userId = GetUserId(email)
        table1=os.getenv("MYSQL_INVENTORY_TABLE")
        table2=os.getenv("MYSQL_LOGIN_TABLE")

        command = f'''
                    SELECT SUM(prod_price) AS Total_spend
                    FROM {table1}
                    INNER JOIN {table2} ON {table1}.user_id = {table2}.Sno
                    WHERE user_id = %s
                    AND MONTH({table1}.prod_add_date) = MONTH(NOW()) AND YEAR({table1}.prod_add_date) = YEAR(NOW());

                '''
        MyCursor.execute(command,(userId,))
        ThisMonth = MyCursor.fetchone()
        # print("This month spend info:",ThisMonth)
        return ThisMonth
    except Exception as e:
        print("\nInfo cannot be rertived from db error in DashboardInfo.py in LatestAdded():-\n",str(e))
        ThisMonth = ["N/A"]
        return ThisMonth




if __name__ == "__main__":
    # info = ProductsInfo("piyush")
    # print(info[0])
    # print(info[1])
    # print(info[2])
    # print(info[3])
    # print(info[4])
    # infoLow = LowStockedInfo("piyush")
    # if infoLow:
    #     print(infoLow)
    # else:
    #     print("no infoLow")
    # info = LatestAdded("piyush")
    # for i in info:
    #     print(i)
    # info = SummaryInfoMonth("piyush")
    # print(info[0])
    pass
