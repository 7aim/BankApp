import json
import datetime
import hashlib
import os

users = {}
logged_in_user = None

# --------------- Utility Functions ---------------
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_directory():
    os.makedirs("db", exist_ok=True)

# --------------- Database Operations ---------------
def load_transactions():
    create_directory()
    try:
        with open("db/transactions.txt", 'r+') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def save_transaction(transaction_data):
    create_directory()
    with open("db/transactions.txt", 'a') as f:
        f.write(transaction_data)

def load_users():
    global users
    create_directory()
    try:
        with open("db/accounts.json", 'r') as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

def save_users():
    create_directory()
    with open("db/accounts.json", 'w') as f:
        json.dump(users, f, indent=4)

def load_session():
    create_directory()
    try:
        with open("db/session.json", 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_session():
    create_directory()
    with open("db/session.json", 'w') as f:
        json.dump(logged_in_user, f, indent=4)

# --------------- Commission Handling ---------------
def load_commission():
    create_directory()
    try:
        with open("db/commission.json", 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"type": "fixed", "value": 1.0}

def save_commission(commission_type, value):
    create_directory()
    with open("db/commission.json", 'w') as f:
        json.dump({"type": commission_type, "value": value}, f)


# --------------- Account Management ---------------
def create_account():
    global users
    load_users()
    
    full_name = input("Full name: ")
    while full_name in users:
        print("Username already exists!")
        full_name = input("Full name: ")

    password = input("Password: ")
    while len(password) < 5:
        print("Password must be at least 5 characters!")
        password = input("Password: ")

    card_number = input("Card number (16 digits): ")
    while len(card_number) != 16 or not card_number.isdigit():
        print("Invalid card number!")
        card_number = input("Card number: ")

    secure_3d = input("Set 3D Secure password: ")
    while len(secure_3d) < 4:
        print("3D password must be at least 4 characters!")
        secure_3d = input("3D Secure password: ")

    # Set role (first user becomes Manager)
    role = "Customer"
    if not users:
        role = "Manager"

    users[full_name] = {
        "id": len(users) + 1,
        "password": hash_password(password),
        "card_number": card_number,
        "balance": 0.0,
        "transactions": [],
        "role": role,
        "3d_secure": hash_password(secure_3d),
    }
    save_users()
    print("Account created successfully!")

# --------------- Authentication ---------------
def login():
    global logged_in_user
    load_users()
    
    username = input("Username: ")
    while username not in users:
        print("User not found!")
        username = input("Username: ")

    password = input("Password: ")
    while hash_password(password) != users[username]["password"]:
        print("Incorrect password!")
        password = input("Password: ")

    logged_in_user = username
    save_session()

# --------------- Banking Operations ---------------
def deposit():
    amount = float(input("Deposit amount: "))
    if amount <= 0:
        print("Amount must be positive!")
        return
    
    users[logged_in_user]["balance"] += amount
    save_users()
    
    transaction = f"{datetime.datetime.now()} | DEPOSIT | +{amount} | Balance: {users[logged_in_user]['balance']}\n"
    save_transaction(transaction)
    print("Deposit successful!")

def withdraw():
    amount = float(input("Withdrawal amount: "))
    if amount <= 0:
        print("Amount must be positive!")
        return
    
    if users[logged_in_user]["balance"] < amount:
        print("Insufficient funds!")
        return
    
    users[logged_in_user]["balance"] -= amount
    save_users()
    
    transaction = f"{datetime.datetime.now()} | WITHDRAW | -{amount} | Balance: {users[logged_in_user]['balance']}\n"
    save_transaction(transaction)
    print("Withdrawal successful!")

def transfer():
    recipient = input("Recipient username: ")
    if recipient not in users:
        print("Recipient not found!")
        return
    
    # 3D Secure Verification
    secure_3d = input("3D Secure password: ")
    if hash_password(secure_3d) != users[logged_in_user]["3d_secure"]:
        print("3D Security verification failed!")
        return
    
    amount = float(input("Transfer amount: "))
    if amount <= 0:
        print("Amount must be positive!")
        return
    
    # Calculate commission
    commission = load_commission()
    if commission["type"] == "fixed":
        fee = commission["value"]
    else:
        fee = amount * (commission["value"] / 100)
    
    total = amount + fee
    
    if users[logged_in_user]["balance"] < total:
        print(f"Insufficient funds! Needed: {total} (including {fee} fee)")
        return
    
    # Perform transfer
    users[logged_in_user]["balance"] -= total
    users[recipient]["balance"] += amount
    save_users()
    
    # Record transactions
    timestamp = datetime.datetime.now()
    sender_transaction = f"{timestamp} | TRANSFER | -{total} | To: {recipient} | Balance: {users[logged_in_user]['balance']}\n"
    recipient_transaction = f"{timestamp} | RECEIVED | +{amount} | From: {logged_in_user} | Balance: {users[recipient]['balance']}\n"
    save_transaction(sender_transaction + recipient_transaction)
    print("Transfer successful!")

# --------------- Admin Functions ---------------
def admin_panel():
    print("\nADMIN PANEL")
    print("2. Manage Commission")
    print("3. View All Users")
    choice = input("Select option: ")

    if choice == "1":
        print("\nCurrent Commission Settings:")
        commission = load_commission()
        print(f"Type: {commission['type'].capitalize()}")
        print(f"Value: {commission['value']}")
        
        new_type = input("Enter new type (fixed/percent): ").lower()
        while new_type not in ["fixed", "percent"]:
            print("Invalid commission type!")
            new_type = input("Enter new type (fixed/percent): ").lower()
        
        new_value = float(input("Enter new value: "))
        save_commission(new_type, new_value)
        print("Commission settings updated!")
    
    elif choice == "2":
        print("\nRegistered Users:")
        for user in users:
            print(f"- {user} ({users[user]['role']})")

# --------------- Main Interface ---------------
def main_menu():
    while True:
        print("\nMAIN MENU")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Select option: ")
        
        if choice == "1":
            create_account()
        elif choice == "2":
            login()
            logged_in_menu()
        elif choice == "3":
            exit()
        else:
            print("Invalid choice!")

def logged_in_menu():
    global logged_in_user
    while True:
        user = users[logged_in_user]
        print(f"\nWelcome, {logged_in_user} ({user['role']})")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Transfer")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Change Password")
        if user["role"] == "Manager":
            print("7. Admin Panel")
        print("8. Logout")
        
        choice = input("Select option: ")
        
        if choice == "1":
            deposit()
        elif choice == "2":
            withdraw()
        elif choice == "3":
            transfer()
        elif choice == "4":
            print(f"\nCurrent Balance: {user['balance']:.2f}")
        elif choice == "5":
            print("\nTRANSACTION HISTORY:")
            print(load_transactions())
        elif choice == "6":
            new_password = input("New password: ")
            while len(new_password) < 5:
                print("Password too short!")
                new_password = input("New password: ")
            user["password"] = hash_password(new_password)
            save_users()
            print("Password changed!")
        elif choice == "7" and user["role"] == "Manager":
            admin_panel()
        elif choice == "8":
            logged_in_user = None
            save_session()
            return
        else:
            print("Invalid option!")

main_menu()