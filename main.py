
# A very simple Flask Hello World app for you to get started with...

from flask import Flask,render_template,request,flash,jsonify
from flask_mysqldb import MySQL
import datetime




app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# config
app.config['MYSQL_HOST']='youredufriends1.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER']='youredufriends1'
app.config['MYSQL_PASSWORD']='vinay1003'
app.config['MYSQL_DB']='youredufriends1$yef'

mysql=MySQL(app)



@app.route('/')
def index():
    return render_template('index.html')





@app.route('/Product/',methods=['GET','POST'])
def product():
    if request.method=='POST':
        Product=request.form
        product_id=Product['product']

        cur=mysql.connection.cursor()
        try:
            result=cur.execute("INSERT INTO Product(product_id) VALUES(%s)",(product_id))
            cur.execute("INSERT INTO InventoryStatus(product_id) VALUES(%s)",(product_id))

            mysql.connection.commit()
            cur.close()
            flash('Product Added Successfully')
            return render_template('Product.html')
        except Exception as e:
            flash('Got Error')
            return render_template('Product.html')


    if request.method=='GET':
        return render_template('Product.html')
    return render_template('Product.html')



@app.route("/Product/product/",methods=['GET','POST'])
def product_list():
    cur=mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Product")
    if resultValue>0:
        Products = cur.fetchall()
        cur.close()
        return render_template('Product.html',Products=Products)
    return str(resultValue)


@app.route('/Location/',methods=['GET','POST'])
def location():
    if request.method=='POST':
        Location=request.form
        location=Location['location_id']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO Location(location) VALUES(%s)",(location,))
        sql="ALTER TABLE InventoryStatus ADD " +location+ " INT(10) not null "
        cur.execute(sql)
        mysql.connection.commit()
        cur.close()
        flash('Location Added Successfully')
        return render_template('Location.html')
    if request.method=='GET':
        return render_template('Location.html')
    return render_template('Location.html')


@app.route("/Location/details/",methods=['GET','POST'])
def location_list():
    cur=mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Location")
    if resultValue>0:
        Locations = cur.fetchall()
        cur.close()
        return render_template('Location.html',Locations=Locations)
    return str(resultValue)


@app.route("/MoveProduct/",methods=['GET','POST'])
def move_product():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM Location")
    Locations_from = cur.fetchall()
    cur.execute("SELECT * FROM Location")
    Locations_to = cur.fetchall()
    cur.execute("SELECT * FROM Product")
    Products = cur.fetchall()
    cur.close()
    return jsonify(Products,Locations_from,Locations_to);
#    return render_template('ProductMovement.html',Locations_from=Locations_from,Locations_to=Locations_to,Products=Products)



@app.route('/ProductMovement/',methods=['GET','POST'])
def product_movement():
    if request.method=='POST':
        ProductMovement=request.form
        location_from=ProductMovement['location_from']
        location_to=ProductMovement['location_to']
        product=ProductMovement['product']
        quantity=ProductMovement['qty']
        cur=mysql.connection.cursor()
        if location_from:
            sql1="update InventoryStatus set "+location_from+"=("+location_from+"-"+quantity+") where product_id=%s"
            cur.execute(sql1,(product,))
        if location_to:
            sql2="update InventoryStatus set "+location_to+"=("+location_to+"+"+quantity+") where product_id=%s"
            cur.execute(sql2,(product,))


        cur.execute("INSERT INTO ProductMovement(timestamp,from_location,to_location,product_id,quantity) VALUES(%s,%s,%s,%s,%s)",(datetime.datetime.now(),location_from,location_to,product,quantity))

        mysql.connection.commit()
        cur.close()
        flash('product Moved sucessfully')
        return render_template('ProductMovement.html')
    if request.method=='GET':
        return render_template('ProductMovement.html')
    return render_template('ProductMovement.html')



@app.route("/ProductMovement/details/",methods=['GET','POST'])
def movement():
    cur=mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM ProductMovement")
    if resultValue>0:
        Locations = cur.fetchall()
        cur.close()
        return render_template('ProductMovement.html',Locations=Locations)
    return str(resultValue)


@app.route("/Report/",methods=['GET','POST'])
def report():
    cur=mysql.connection.cursor()
    resultValue= cur.execute("select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='InventoryStatus';")

    if resultValue>0:
        Columns = cur.fetchall()
        cur.execute("SELECT * FROM InventoryStatus")
        Locations = cur.fetchall()
        cur.close()
        return render_template('Report.html',Columns=Columns,list1=resultValue,Locations=Locations)
    return str(resultValue)


if(__name__)=='__main__':
    app.run(debug=True)
