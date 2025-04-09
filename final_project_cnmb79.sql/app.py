#import modules
from flask import Flask, render_template, request, flash, url_for, redirect
import mysql.connector
from mysql.connector import errorcode
import pygal

#create a flask app object and set app variables
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = 'your secret key'
app.secret_key = 'your secret key'

#create a connection object to the sakila database
def get_db_connection():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            port="6603",
            database="sakila"
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password.")
            exit()
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
            exit()
        else:
            print(err)
            print("ERROR: Service not available")
            exit()

    return mydb

#functions




#pygal graph
def create_graph(labels, values, chart_title):
    chart_object = pygal.Bar(x_label_rotation=45, height=500)
    chart_object.title = chart_title
    chart_object.x_labels = labels
    chart_object.add("orders", values)
    return chart_object.render_data_uri()


#monthly rental sales
def monthlyRentalSales(year):
        #get a connection to the database
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)
        query = '''SELECT month_num, month, TotalPayments
                    FROM monthlyRentalSales
                    WHERE year = %s
                    ORDER BY month_num;'''
        cursor.execute(query,(year,))
        results=cursor.fetchall()
        cursor.close()
        mydb.close()
        labels= [str(row['month']) for row in results]  
        values= [row['TotalPayments'] for row in results]
        chart_title= "Sales by month"
        chart = create_graph(labels, values, chart_title)
        table_data = [{"month": row['month'], "Total Payments": row['TotalPayments']} for row in results]
        return chart, "Sales by month", table_data

#category totals
def categoryTotals(year):
        #get a connection to the database
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)
        query='''SELECT name, TotalPayments
                FROM categoryTotals
                WHERE year = %s
                ORDER BY TotalPayments;'''
        cursor.execute(query,(year,))
        results=cursor.fetchall()
        cursor.close()
        mydb.close()
        labels= [row['name'] for row in results]  
        values= [row['TotalPayments'] for row in results]
        chart_title= "Sales by category"
        chart= create_graph(labels, values, chart_title)
        table_data = [{"Name": row['name'], "Total Payments": row['TotalPayments']} for row in results]
        return chart, "Sales by category", table_data

#store city sales
def storeCitySales(year):
        #get a connection to the database
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)
        query='''SELECT city, TotalPayments
                FROM storeCitySales
                WHERE year = %s
                ORDER BY TotalPayments;'''
        cursor.execute(query,(year,))
        results=cursor.fetchall()
        cursor.close()
        mydb.close()
        labels= [row['city'] for row in results]  
        values= [row['TotalPayments'] for row in results]
        chart_title= "Sales by city"
        chart = create_graph(labels, values, chart_title)
        table_data = [{"City": row['city'], "Total Payments": row['TotalPayments']} for row in results]
        return chart, "Sales by city", table_data

#customer rental sales
def customerRentalSales(year):
        #get a connection to the database
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)
        query = '''SELECT name, TotalPayments
                 FROM customerRentalSales
                 WHERE year = %s
                 ORDER BY TotalPayments DESC
                 LIMIT 15;'''
        cursor.execute(query,(year,))
        results = cursor.fetchall()
        cursor.close()
        mydb.close()
        labels= [row['name'] for row in results]  
        values= [row['TotalPayments'] for row in results]
        chart_title= "Customer Sales Totals: Top 15"
        chart = create_graph(labels, values, chart_title)
        table_data = [{"Name": row['name'], "Total Payments": row['TotalPayments']} for row in results]
        return chart, "Customer Sales Totals: Top 15", table_data

#customer movie rentals
def customerMovieRentals(year):
        #get a connection to the database
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)
        query= '''SELECT name, numRentals
                 FROM customerMovieRentals
                 WHERE year =%s
                 ORDER BY numRentals DESC
                 LIMIT 15;'''
        cursor.execute(query,(year,))
        results = cursor.fetchall()
        cursor.close()
        mydb.close()
        labels= [row['name'] for row in results]  
        values= [row['numRentals'] for row in results]
        chart_title= "Customer Rental Totals: Top 15"
        chart = create_graph(labels, values, chart_title)
        table_data = [{"Name": row['name'], "Number of rentals": row['numRentals']} for row in results]
        return chart, "Customer Rental Totals: Top 15", table_data

#movies per category
def moviesPerCategory():
        #get a connection to the database
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)
        query='''SELECT name, numMovies
                 FROM moviesPerCategory
                 ORDER BY numMovies;'''
        cursor.execute(query,)
        results = cursor.fetchall()
        cursor.close()
        mydb.close()
        labels= [row['name'] for row in results]  
        values= [row['numMovies'] for row in results]
        chart_title= "movies per category"
        chart = create_graph(labels, values, chart_title)
        table_data = [{"Name": row['name'], "Number of Movies": row['numMovies']} for row in results]
        return chart, "movies per category", table_data

#movies per category in stock
def moviesPerCategoryInStock():
        #get a connection to the database
        mydb = get_db_connection()
        cursor = mydb.cursor(dictionary=True)
        query= '''SELECT name, numMovies
                 FROM moviesPerCategoryInStock
                 ORDER BY numMovies;'''
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        mydb.close()
        labels= [row['name'] for row in results]  
        values= [row['numMovies'] for row in results]
        chart_title= "movies per category in stock"
        chart = create_graph(labels, values, chart_title)
        table_data=[{"Name": row['name'], "Number of Movies": row['numMovies']} for row in results]
        return chart, "movies per category in stock", table_data

def get_years():
    #get a connection to the database
    mydb = get_db_connection()
    cursor = mydb.cursor()
    cursor.execute("SELECT DISTINCT YEAR(rental_date) FROM rental ORDER BY YEAR(rental_date) DESC")
    years=[year[0] for year in cursor.fetchall()]
    cursor.close()
    mydb.close()
    return years




#Routes



#Home route
@app.route('/', methods=['GET', 'POST'])
def home():
    error= None
    if request.method=='POST':
        report_choice=request.form.get('report_choice')
        if not report_choice:error= "You must choose a report"
        else:
            if report_choice== 'rental-reports':
                return redirect(url_for('rental_reports'))
            elif report_choice== 'customer-reports':
                return redirect(url_for('customer_reports'))
            elif report_choice== 'inventory-reports':
                return redirect(url_for('inventory_reports'))
    return render_template('index.html', error=error)


#rental reports
@app.route('/rental-reports', methods=['GET', 'POST'])
def rental_reports():
    years= get_years()  
    chart= None
    chart_title= None
    table_data=None
    error= None
    if request.method== 'POST':
        report_choice=request.form.get('report_choice')
        selected_year= request.form.get('year')
        if not report_choice:error= "You must choose a report"
        elif not selected_year:error="You must choose a year"
        else:
            if report_choice=='monthly_sales':
                chart, chart_title, table_data = monthlyRentalSales(selected_year)
            elif report_choice== 'sales_by_category':
                chart, chart_title, table_data = categoryTotals(selected_year)
            elif report_choice == 'sales_by_city':
                chart, chart_title, table_data = storeCitySales(selected_year)

    return render_template('rental.html', years=years, chart=chart, chart_title=chart_title, table_data=table_data,error=error)




#customer reports
@app.route('/customer-reports', methods=['GET', 'POST'])
def customer_reports():
    years=get_years()  
    chart= None
    chart_title= None
    table_data=None
    error= None
    if request.method== 'POST':
        report_choice=request.form.get('report_choice')
        selected_year= request.form.get('year')
        if not report_choice:error= "You must choose a report"
        elif not selected_year:error="You must choose a year"
        else:
            if report_choice=='customer_sales_totals':
                chart, chart_title, table_data= customerRentalSales(selected_year)
            elif report_choice=='customer_rental_totals':
                chart, chart_title, table_data= customerMovieRentals(selected_year)

    return render_template('customers.html', years=years, chart=chart, chart_title=chart_title, table_data=table_data,error=error)


#inventory reports
@app.route('/inventory-reports', methods=['GET', 'POST'])
def inventory_reports():
    chart= None
    chart_title= None
    table_data=None
    error= None
    if request.method== 'POST':
        report_choice= request.form.get('report_choice')
        if not report_choice:error= "You must choose a report"
        else:
            if report_choice== 'moviesPerCategory':
                chart, chart_title, table_data = moviesPerCategory()
            elif report_choice== 'moviesPerCategoryInStock':
                chart, chart_title, table_data = moviesPerCategoryInStock()
    return render_template('inventory.html', chart=chart, chart_title=chart_title, table_data=table_data,error=error)





app.run(port=5011, debug=True)