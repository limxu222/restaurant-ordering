from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Sample menu
menu = [
    {"name": "Nasi Lemak", "price": 6.50},
    {"name": "Mee Goreng", "price": 5.00},
    {"name": "Teh Tarik", "price": 2.00}
]

# Create DB if not exists
conn = sqlite3.connect('orders.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, name TEXT, items TEXT)''')
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('index.html', menu=menu)

@app.route('/order', methods=['POST'])
def order():
    name = request.form['name']
    items = request.form.getlist('item')
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("INSERT INTO orders (name, items) VALUES (?, ?)", (name, ", ".join(items)))
    conn.commit()
    conn.close()
    return render_template('order_success.html', name=name, items=items)

@app.route('/admin')
def admin():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders")
    orders = c.fetchall()
    conn.close()
    return render_template('admin.html', orders=orders)

@app.route('/delete/<int:order_id>')
def delete(order_id):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
