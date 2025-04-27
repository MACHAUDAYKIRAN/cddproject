from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',  # Use localhost if running outside Docker
        user='root',
        password='Uday@123',
        database='agriculture_management'
    )
    return conn

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Add Product route
@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Get form data from user
        product_name = request.form['product_name']
        product_type = request.form['product_type']
        price = request.form['price']

        # Connect to the database and insert the new product
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO products (product_name, product_type, price) VALUES (%s, %s, %s)',
                       (product_name, product_type, price))
        conn.commit()
        cursor.close()
        conn.close()

        # Redirect to the view products page
        return redirect(url_for('view_products'))

    return render_template('add_product.html')

# View Products route
@app.route('/view-products')
def view_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('view_products.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
