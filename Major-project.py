#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sqlite3

# Database connection
conn = sqlite3.connect("atm.db")
cur = conn.cursor()

# Table create (run once)
cur.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    acc_no INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    pin TEXT,
    balance REAL
)
''')
conn.commit()

# Create new account
def create_account():
    name = input("Enter your name: ")
    pin = input("Set a 4-digit PIN: ")
    balance = float(input("Enter initial deposit: ₹"))
    cur.execute("INSERT INTO accounts (name, pin, balance) VALUES (?, ?, ?)", (name, pin, balance))
    conn.commit()
    
    # Get the account number of the last inserted account
    acc_no = cur.lastrowid
    print("✅ Account created successfully!")
    print(f"🧾 Your Account Number is: {acc_no} — Please save it for login.")

# Login
def login(acc_no, pin):
    cur.execute("SELECT * FROM accounts WHERE acc_no=? AND pin=?", (acc_no, pin))
    user = cur.fetchone()
    if user:
        print(f"\n👋 Welcome {user[1]}!")
        return user
    else:
        print("❌ Invalid account number or PIN.")
        return None

# Check balance
def check_balance(acc_no):
    cur.execute("SELECT balance FROM accounts WHERE acc_no=?", (acc_no,))
    balance = cur.fetchone()[0]
    print(f"💰 Current Balance: ₹{balance}")     

# Deposit money
def deposit(acc_no, amount):
    cur.execute("UPDATE accounts SET balance = balance + ? WHERE acc_no=?", (amount, acc_no))
    conn.commit()
    print(f"✅ ₹{amount} deposited successfully.")    

# Withdraw money
def withdraw(acc_no, amount):
    cur.execute("SELECT balance FROM accounts WHERE acc_no=?", (acc_no,))
    current_balance = cur.fetchone()[0]
    if amount > current_balance:
        print("❌ Insufficient balance!")
    else:
        cur.execute("UPDATE accounts SET balance = balance - ? WHERE acc_no=?", (amount, acc_no))
        conn.commit()
        print(f"✅ ₹{amount} withdrawn successfully.")    

# ATM menu after login
def atm_menu(acc_no):
    while True:
        print("\n--- ATM Menu ---")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            check_balance(acc_no)
        elif choice == '2':
            amt = float(input("Enter amount to deposit: ₹"))
            deposit(acc_no, amt)
        elif choice == '3':
            amt = float(input("Enter amount to withdraw: ₹"))
            withdraw(acc_no, amt)
        elif choice == '4':
            print("👋 Thank you for using the ATM. Bye!")
            break
        else:
            print("❌ Invalid choice.")

# Main menu
def main():
    print("===== 🏧 Welcome to Python ATM =====")
    print("1. Create Account")
    print("2. Login")
    choice = input("Enter your choice: ")

    if choice == '1':
        create_account()
    elif choice == '2':
        try:
            acc_no = int(input("Enter Account Number: "))
            pin = input("Enter PIN: ")
            user = login(acc_no, pin)
            if user:
                atm_menu(acc_no)
        except ValueError:
            print("❌ Invalid input. Account number must be a number.")
    else:
        print("❌ Invalid choice. Exiting...")

main()
conn.close()


# In[ ]:




