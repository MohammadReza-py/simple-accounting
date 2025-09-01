# 🧾 Simple Accounting Desktop App  

A **basic accounting desktop application** built with **Python (Tkinter + SQLite)**.  
This project was developed as a **learning and practice project** to demonstrate skills in:  
- GUI development using **Tkinter**  
- Database design & CRUD operations with **SQLite**  
- Structuring a desktop application with multiple pages (Invoices, Transactions, Reports, Definitions)  
- Displaying data with **Treeview reports**  

⚠️ **Important Notice**  
This project is **for educational and demonstration purposes only**.  
It is **not intended for real-world accounting use**.  
The code is intentionally kept **simple and beginner-friendly** to make it easy to understand and showcase basic programming concepts.  

---

## ✨ Features
- 📄 Create and manage **invoices** (buy/sell)  
- 💰 Record **payments and receipts**  
- 👥 Define **persons** (customers/vendors) and **products**  
- 📊 Generate **reports** (invoices & transactions) with a simple GUI table  
- 🎨 Styled interface using **ttk.Style** for a cleaner look  

---

## 🛠️ Tech Stack
- **Python 3.x**  
- **Tkinter** (for GUI)  
- **SQLite** (for database)  

---

## 🚀 How to Run
1. Clone the repository  
```bash
   git clone https://github.com/your-username/simple-accounting-app.git
   cd simple-accounting-app
```
2. Run the app
  ```bash
    python app.py
  ```
3. The database (```accounting.db```) will be automatically created on first run.

## 🧪 Using the Custom Faker Package

This project includes a **custom-built Faker package** designed to generate **fake/sample data** for testing the application.  

### What is this Faker?
- This is a **personal implementation**, created from scratch without using any external libraries or packages.  
- It generates realistic **sample persons, products, invoices, and transactions** for testing purposes.  

### Why use it?
- To **populate the database quickly** with sample data without manually entering everything.  
- To **test the application features**, reports, and interface with realistic-looking data.  
- To help users **practice and explore the app** more efficiently.  

### How to use it
1. The Faker package is **completely separate** from the main application.  
2. Run the Faker script independently to **add sample data** to your `accounting.db` database.  
3. You can customize the **number and type of generated records** before running it.  
4. After generating data, open the main app (`app.py`) to explore the application with pre-filled sample data.  

> ⚠️ Note: Using the Faker package is **optional**. It's intended purely for testing and demonstration. The main application works perfectly fine without it.


## 📌 Notes

✅ This project is educational and aims to showcase programming skills, not to replace real accounting systems.

✅ The code is kept clear and simple to help beginners understand core concepts.

✅ Contributions & suggestions for improvement are welcome!
