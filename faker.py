import sqlite3
import random

# ---------- base data ----------
first_names = ["علی", "رضا", "محمد", "سارا", "زهرا", "مهسا", "حسین", "نگار", "آرمان", "مینا"]
last_names = ["احمدی", "کاظمی", "موسوی", "نجفی", "پورمحمد", "رحیمی", "سلیمانی", "نوری"]
product_names = ["کاغذ", "خودکار", "دفتر", "چسب", "ماژیک", "پرینتر", "مانیتور", "کیبورد", "موس", "کابل"]

person_types = ["customer", "vendor"]
invoice_types = ["buy", "sell"]
transaction_types = ["pay", "receive"]

# ---------- connecting to the database ----------
conn = sqlite3.connect("accounting.db")
c = conn.cursor()

# ---------- add person ----------
def add_persons(n=10):
    for _ in range(n):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        type_person = random.choice(person_types)
        c.execute("INSERT INTO persons(name,type) VALUES(?,?)", (name, type_person))
    conn.commit()

# ---------- add product ----------
def add_products(n=10):
    for _ in range(n):
        name = random.choice(product_names) + str(random.randint(1, 50))
        price = round(random.uniform(50, 5000), 2)
        c.execute("INSERT INTO products(name,price) VALUES(?,?)", (name, price))
    conn.commit()

# ---------- add invoic  ----------
def add_invoices(n=20):
    c.execute("SELECT id FROM persons")
    person_ids = [row[0] for row in c.fetchall()]
    c.execute("SELECT id FROM products")
    product_ids = [row[0] for row in c.fetchall()]

    for _ in range(n):
        person_id = random.choice(person_ids)
        product_id = random.choice(product_ids)
        qty = random.randint(1, 20)
        inv_type = random.choice(invoice_types)
        c.execute("SELECT price FROM products WHERE id=?", (product_id,))
        price = c.fetchone()[0]
        total = price * qty
        c.execute("INSERT INTO invoices(person_id,product_id,qty,total,type) VALUES(?,?,?,?,?)",
                  (person_id, product_id, qty, total, inv_type))
    conn.commit()

# ---------- add transaction ----------
def add_transactions(n=20):
    c.execute("SELECT id FROM persons")
    person_ids = [row[0] for row in c.fetchall()]

    for _ in range(n):
        person_id = random.choice(person_ids)
        amount = round(random.uniform(100, 10000), 2)
        tr_type = random.choice(transaction_types)
        c.execute("INSERT INTO transactions(person_id,amount,type) VALUES(?,?,?)",
                  (person_id, amount, tr_type))
    conn.commit()

# ---------- run functions ----------
add_persons(15)
add_products(15)
add_invoices(30)
add_transactions(30)

print("✅the test data has created!")
conn.close()
