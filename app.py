from flask import Flask,request,render_template,redirect,url_for,session
from auth.LoginDb import Login
from auth.SignupDb import SignUp
from database.AddProd import AddProd
from database.Retrive import GetUserId,RetriveInfo
from database.DashboardInfo import ProductsInfo,LowStockedInfo,LatestAdded,SummaryInfoMonth
from database.Edit_del import DeleteProd
from dotenv import load_dotenv
import os



app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRETE_KEY")

@app.route('/',methods=['GET','POST'])
def LoginPage():
    if 'email' in session:
        email = session["email"]
        return redirect(url_for("Inventory"))
    else:
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            check = Login(email,password)
            if check == True:
                session['email'] = email
                return redirect(url_for("Inventory"))
            else:
                return render_template('login.html', error="Wrong username or password!")
        else:
            return render_template("login.html",error=None)
        

@app.route('/signup',methods=['GET','POST'])
def SignupPage():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        check_pass = request.form["password_repeat"]
        if password == check_pass:
            check = SignUp(email,password)
            if check == True:
                session['email'] = email
                return redirect(url_for("Inventory"))
            else:
                return render_template("signup.html",error = "User already exist !!")
        else:
            return render_template("signup.html",error = "Please Enter same password !!")
    else:
        return render_template("signup.html",error=None)

@app.route('/inventory',methods=["GET","POST"])
def Inventory():
    if 'email' in session:
        email = session["email"]
        logo = email[0:2]

        products_info_div = ProductsInfo(email)
        Low_stock_info = LowStockedInfo(email)
        Latest_added = LatestAdded(email)
        Total_spend = SummaryInfoMonth(email)

        return render_template("inventory.html",user=email,logo=logo,products_info_div=products_info_div,Low_stock_info=Low_stock_info,Latest_added=Latest_added,Total_spend=Total_spend)
    else:
        return redirect(url_for("LoginPage"))

@app.route("/products",methods=["GET"])
def Products():
    if 'email' in session:
            email = session["email"]
            logo = email[0:2]
            ProductsArray = RetriveInfo(email)

            return render_template("product.html",user=email,logo=logo,prodArr=ProductsArray)
    else:
        return redirect(url_for("LoginPage"))


@app.route("/products",methods = ["post"])
def AddProducts():
    if "email" in session:
        email = session["email"]
        user_id = GetUserId(email)


        product_name = request.form["product_name"]
        product_id = request.form["product_id"]
        product_qty = request.form["product_qty"]
        product_price = request.form["product_price"]
        product_low_qty = request.form["product_low_qty"]
        product_category = request.form["product_category"]
        product_size = request.form["product_size"]
        product_weight = request.form["product_weight"]
        supplier_name = request.form["supplier_name"]
        supplier_no = request.form["supplier_no"]
        item_color = request.form["item_color"]
        item_comments = request.form["item_comments"]
        drop_image = request.files["drop_image"]
        image = drop_image.read()

        prodResp = AddProd(prod_comments=item_comments,prod_color=item_color,prod_low_qty = product_low_qty,prod_size=product_size,prod_weight=product_weight,prod_id = product_id,prod_name = product_name,prod_price=product_price,prod_qty=product_qty,prod_category=product_category,supplier_name=supplier_name,supplier_no=supplier_no,prod_img=image,userid=user_id)

        # print("response in app.py for add product = \n",prodResp)

        return redirect(url_for("Products"))

@app.route("/delete",methods=["post"])
def DeleteRow():
    if "email" in session:
        email = session["email"]
        del_prod_id = request.form.get("del_product_id")
        print("del_prod_id: ",del_prod_id)
        DeleteProd(email,del_prod_id)
        return redirect(url_for("Products"))
    else:
        return redirect(url_for("LoginPage"))
    
@app.route("/product/search")
def SearchProduct():
    pass


@app.route("/logout")
def Logout():
    if "email" in session:
        session.pop('email', None)
        return redirect(url_for("LoginPage"))
    else:
        return "not logged in"
    
@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html")


if __name__ == '__main__':
    app.run(debug=True)