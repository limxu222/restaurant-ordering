from flask import Flask, render_template, request, redirect, abort
import sqlite3
import os

app = Flask(__name__)

DB_FILE = "orders.db"

def init_db():
    if not os.path.exists(DB_FILE):
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute('''
CREATE TABLE orders (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
items TEXT NOT NULL
)
''')

@app.route("/")
def index():
    menu = [
{"id": 1, "name": "Nasi Lemak", "price": 8},
{"id": 2, "name": "Chicken Chop", "price": 15},
{"id": 3, "name": "Iced Milo", "price": 4},
{"id": 4, "name": "Teh Tarik", "price": 3}
]
    return render_template("index.html", menu=menu)

@app.route("/order", methods=["POST"])
def order():
    name = request.form.get("name")
    items = request.form.getlist("item")
    if name and items:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT INTO orders (name, items) VALUES (?, ?)", (name, ", ".join(items)))
        return render_template("order_success.html", name=name, items=items)
    else:
        return "Missing name or items.", 400

@app.route("/admin")
def admin():
    key = request.args.get("key")
    if key != "admin123":
        return abort(403)
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, items FROM orders")
            orders = cursor.fetchall()
        return render_template("admin.html", orders=orders)

@app.route("/delete/int:order_id")
def delete_order(order_id):
    key = request.args.get("key")
    if key != "admin123":
        return abort(403)
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("DELETE FROM orders WHERE id=?", (order_id,))
        return redirect("/admin?key=admin123")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)

