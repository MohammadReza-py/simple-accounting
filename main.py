import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------- Database ----------
def init_db():
    conn = sqlite3.connect("accounting.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS persons(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS invoices(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        product_id INTEGER,
        qty INTEGER,
        total REAL,
        type TEXT NOT NULL,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(product_id) REFERENCES products(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER,
        amount REAL,
        type TEXT NOT NULL,
        FOREIGN KEY(person_id) REFERENCES persons(id)
    )""")
    conn.commit()
    conn.close()

# ---------- Base App ----------
class AccountingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("نرم افزار حسابداری ساده")
        self.geometry("600x400")

        style = ttk.Style(self)
        style.configure("TButton", font=("Arial", 12), padding=6)
        style.configure("TLabel", font=("Arial", 11))

        self.frames = {}
        for F in (MainMenu, InvoicesPage, TransactionsPage, DefinitionsPage, ReportsPage):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainMenu)

    def show_frame(self, page):
        self.frames[page].tkraise()

# ---------- Main Menu ----------
class MainMenu(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        ttk.Label(self, text="منوی اصلی", font=("Arial", 18, "bold")).pack(pady=20)

        ttk.Button(self, text="📄 فاکتور", width=20, command=lambda: master.show_frame(InvoicesPage)).pack(pady=10)
        ttk.Button(self, text="💰 پرداخت/دریافت", width=20, command=lambda: master.show_frame(TransactionsPage)).pack(pady=10)
        ttk.Button(self, text="⚙️ تعاریف", width=20, command=lambda: master.show_frame(DefinitionsPage)).pack(pady=10)
        ttk.Button(self, text="📊 گزارش", width=20, command=lambda: master.show_frame(ReportsPage)).pack(pady=10)

# ---------- Invoices ----------
class InvoicesPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        ttk.Label(self, text="ثبت فاکتور", font=("Arial", 16)).pack(pady=10)

        form = ttk.Frame(self)
        form.pack(pady=10)
        ttk.Label(form, text="شناسه شخص:").grid(row=0, column=0, sticky="w")
        self.person_id = ttk.Entry(form)
        self.person_id.grid(row=0, column=1, padx=5)

        ttk.Label(form, text="شناسه محصول:").grid(row=1, column=0, sticky="w")
        self.product_id = ttk.Entry(form)
        self.product_id.grid(row=1, column=1, padx=5)

        ttk.Label(form, text="تعداد:").grid(row=2, column=0, sticky="w")
        self.qty = ttk.Entry(form)
        self.qty.grid(row=2, column=1, padx=5)

        ttk.Label(form, text="نوع (buy/sell):").grid(row=3, column=0, sticky="w")
        self.inv_type = ttk.Entry(form)
        self.inv_type.grid(row=3, column=1, padx=5)

        ttk.Button(self, text="ثبت فاکتور", command=self.add_invoice).pack(pady=10)
        ttk.Button(self, text="⬅️ بازگشت", command=lambda: master.show_frame(MainMenu)).pack()

    def add_invoice(self):
        conn = sqlite3.connect("accounting.db")
        c = conn.cursor()
        c.execute("SELECT price FROM products WHERE id=?", (self.product_id.get(),))
        price = c.fetchone()
        if price:
            total = int(self.qty.get()) * price[0]
            c.execute("INSERT INTO invoices(person_id,product_id,qty,total,type) VALUES(?,?,?,?,?)",
                      (self.person_id.get(), self.product_id.get(), self.qty.get(), total, self.inv_type.get()))
            conn.commit()
            messagebox.showinfo("موفق", f"فاکتور ذخیره شد ✅\nمبلغ کل: {total}")
        else:
            messagebox.showerror("خطا", "محصول یافت نشد")
        conn.close()

# ---------- Transactions ----------
class TransactionsPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        ttk.Label(self, text="پرداخت / دریافت", font=("Arial", 16)).pack(pady=10)

        form = ttk.Frame(self)
        form.pack(pady=10)
        ttk.Label(form, text="شناسه شخص:").grid(row=0, column=0, sticky="w")
        self.person_id = ttk.Entry(form)
        self.person_id.grid(row=0, column=1)

        ttk.Label(form, text="مبلغ:").grid(row=1, column=0, sticky="w")
        self.amount = ttk.Entry(form)
        self.amount.grid(row=1, column=1)

        ttk.Label(form, text="نوع (pay/receive):").grid(row=2, column=0, sticky="w")
        self.tr_type = ttk.Entry(form)
        self.tr_type.grid(row=2, column=1)

        ttk.Button(self, text="ثبت تراکنش", command=self.add_transaction).pack(pady=10)
        ttk.Button(self, text="⬅️ بازگشت", command=lambda: master.show_frame(MainMenu)).pack()

    def add_transaction(self):
        conn = sqlite3.connect("accounting.db")
        c = conn.cursor()
        c.execute("INSERT INTO transactions(person_id,amount,type) VALUES(?,?,?)",
                  (self.person_id.get(), self.amount.get(), self.tr_type.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("موفق", "تراکنش ثبت شد ✅")

# ---------- Definitions ----------
class DefinitionsPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        ttk.Label(self, text="تعاریف (اشخاص و محصولات)", font=("Arial", 16)).pack(pady=10)

        ttk.Label(self, text="نام شخص:").pack()
        self.person_name = ttk.Entry(self)
        self.person_name.pack()
        ttk.Label(self, text="نوع (customer/vendor):").pack()
        self.person_type = ttk.Entry(self)
        self.person_type.pack()
        ttk.Button(self, text="➕ افزودن شخص", command=self.add_person).pack(pady=5)

        ttk.Label(self, text="نام محصول:").pack()
        self.product_name = ttk.Entry(self)
        self.product_name.pack()
        ttk.Label(self, text="قیمت:").pack()
        self.product_price = ttk.Entry(self)
        self.product_price.pack()
        ttk.Button(self, text="➕ افزودن محصول", command=self.add_product).pack(pady=5)

        ttk.Button(self, text="⬅️ بازگشت", command=lambda: master.show_frame(MainMenu)).pack(pady=10)

    def add_person(self):
        conn = sqlite3.connect("accounting.db")
        c = conn.cursor()
        c.execute("INSERT INTO persons(name,type) VALUES(?,?)",
                  (self.person_name.get(), self.person_type.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("موفق", "شخص ثبت شد ✅")

    def add_product(self):
        conn = sqlite3.connect("accounting.db")
        c = conn.cursor()
        c.execute("INSERT INTO products(name,price) VALUES(?,?)",
                  (self.product_name.get(), self.product_price.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("موفق", "محصول ثبت شد ✅")

# ---------- Reports ----------
class ReportsPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=20)
        ttk.Label(self, text="گزارشات", font=("Arial", 16)).pack(pady=10)

        ttk.Button(self, text="📄 گزارش فاکتورها", command=self.show_invoices).pack(pady=5)
        ttk.Button(self, text="💰 گزارش تراکنش‌ها", command=self.show_transactions).pack(pady=5)
        self.tree = ttk.Treeview(self, columns=("col1","col2","col3"), show="headings")
        self.tree.pack(pady=10, fill="both", expand=True)

        ttk.Button(self, text="⬅️ بازگشت", command=lambda: master.show_frame(MainMenu)).pack(pady=10)

    def show_invoices(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ("id","person","product","total","type")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        conn = sqlite3.connect("accounting.db")
        c = conn.cursor()
        c.execute("SELECT id, person_id, product_id, total, type FROM invoices")
        for row in c.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def show_transactions(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ("id","person","amount","type")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        conn = sqlite3.connect("accounting.db")
        c = conn.cursor()
        c.execute("SELECT id, person_id, amount, type FROM transactions")
        for row in c.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

# ---------- Run ----------
if __name__ == "__main__":
    init_db()
    app = AccountingApp()
    app.mainloop()
