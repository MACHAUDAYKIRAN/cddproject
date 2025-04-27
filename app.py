from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Function to connect to the database
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',          # your MySQL username (usually root)
        password='Uday@123',  # your MySQL password
        database='agriculture_management'  # name of your database
    )
    return connection

# Add product route
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_type = request.form['product_type']
        price = request.form['price']

        # Ensure price is a valid number
        try:
            price = float(price)
        except ValueError:
            return "Invalid price format, please enter a valid number."

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO products (product_name, product_type, price) VALUES (%s, %s, %s)',
                       (product_name, product_type, price))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect('/view_products')

    return render_template('add_product.html')

@app.route('/')
def home():
    return render_template('home.html')

# View products route
@app.route('/view_products')
def view_products():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('view_products.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
