import sqlite3
import random
import string
import qrcode
import base64
from flask import Flask, render_template, request, redirect, session
from datetime import datetime
from io import BytesIO

app = Flask(__name__)
app.secret_key = "VISHESH_SECRET_KEY"
DB = "food.db"

# ---------------- DB CONNECTION ----------------
def db():
    return sqlite3.connect(DB)

# ---------------- ORDER ID GENERATOR ----------------
def generate_order_id(name):
    chars = string.ascii_letters + string.digits + "@#$"
    rand_part = ''.join(random.choice(chars) for _ in range(6))
    return f"VISH13{name[0].upper()}{rand_part}"

# ================= PUBLIC ROUTES =================

# HOME / MENU
@app.route("/")
def index():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM food")
    foods = cur.fetchall()
    con.close()
    return render_template("index.html", foods=foods)

# ABOUT
@app.route("/about")
def about():
    return render_template("about.html")

# CONTACT
@app.route("/contact")
def contact():
    return render_template("contact.html")

# FEEDBACK (FIXED – NO ERROR)
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]
        time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        con = db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO feedback VALUES (NULL, ?, ?, ?)",
            (name, message, time)
        )
        con.commit()
        con.close()
        return redirect("/")

    return render_template("feedback.html")

# CART PAGE
@app.route("/cart/<int:id>")
def cart(id):
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM food WHERE id=?", (id,))
    item = cur.fetchone()
    con.close()
    return render_template("cart.html", item=item)

# PLACE ORDER (HOME + TABLE + QR)
@app.route("/place_order", methods=["POST"])
def place_order():
    name = request.form["name"]
    order_type = request.form["order_type"]
    address = request.form.get("address", "")
    table_no = request.form.get("table_no", "")
    food = request.form["food"]
    price = request.form["price"]
    time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    order_uid = generate_order_id(name)

    # QR CODE GENERATION
    qr_text = f"ORDER ID: {order_uid}\nNAME: {name}\nFOOD: {food}\nTYPE: {order_type}"
    qr = qrcode.make(qr_text)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    con = db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO orders VALUES (NULL,?,?,?,?,?,?,?,?)",
        (order_uid, name, address, table_no, order_type, food, price, time)
    )
    con.commit()
    con.close()

    return render_template(
        "success.html",
        order_id=order_uid,
        qr=qr_base64
    )

# ORDER HISTORY (CUSTOMER VIEW)
@app.route("/orders")
def orders():
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = cur.fetchall()
    con.close()
    return render_template("orders.html", orders=orders)

# ================= ADMIN ROUTES =================

# ADMIN LOGIN
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form["user"] == "VisheshG" and request.form["pass"] == "Vishesh@Tum":
            session["admin"] = True
            return redirect("/admin_panel")
    return render_template("admin_login.html")

# ADMIN PANEL
@app.route("/admin_panel", methods=["GET", "POST"])
def admin_panel():
    if not session.get("admin"):
        return redirect("/admin")

    con = db()
    cur = con.cursor()

    # ADD FOOD ITEM
    if request.method == "POST":
        cur.execute(
            "INSERT INTO food VALUES (NULL,?,?,?,?)",
            (
                request.form["name"],
                request.form["category"],
                request.form["price"],
                request.form["image"]
            )
        )
        con.commit()

    # FETCH DATA
    cur.execute("SELECT * FROM food")
    foods = cur.fetchall()

    cur.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = cur.fetchall()

    cur.execute("SELECT * FROM feedback ORDER BY id DESC")
    feedbacks = cur.fetchall()

    con.close()

    return render_template(
        "admin_panel.html",
        foods=foods,
        orders=orders,
        feedbacks=feedbacks
    )

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= RUN =================
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
