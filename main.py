import json
import datetime
import hashlib

users = {}
logged_in = None

def hashPassword(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def trLoad():
    with open("db/transaction.txt", 'r') as f:
        return f.read()

def trSave(log_data):
    with open("db/transaction.txt", 'a') as f:
        f.write(log_data)

def userLoad():
    global users
    try:
        with open("db/accounts.json", "r", encoding="utf-8") as f:
            users = json.load(f)
    except:
        users = {}

def userSave(data):
    with open("db/accounts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def loadSession():
    try:
        with open("db/session.json","r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}
    
def saveSession(session_data):
    with open("db/session.json","w") as f:
        json.dump(session_data, f, indent=4)

def createAccount():
    id = len(users) + 1
    name = input("Name : ")
    password = input("Password : ")
    password = hashPassword(password)
    card_no = input("Card Number : ")
    balance = 0
    log = []

    users[name] = {"id" : id,'password': password,"card_no" : card_no,"balance" : balance,"log" : log}
    userSave(users)

    print("Account is created")
    logged_in = name
    saveSession(logged_in)

def signIn():
    global logged_in
    global name

    name = input("Name : ")
    for i in users:     
        while name not in users:
            print("Name not found")
            name = input("Name : ")

    password = hashPassword(input("Password : "))
    while password not in users[name]["password"]:
        print("Password is incorrect")
        password = input("Password : ")

    """card_no = input("Card Number : ")
    while card_no not in users[name]["card_no"]:
        print("Card number is incorrect")
        card_no = input("Card Number : ")"""

    logged_in = name
    saveSession(logged_in)

while True:
    userLoad()
    logged_in = loadSession()

    if not logged_in:
        print("\nHello, Welcome")
        print("[1] Create account")
        print("[2] Sign in")
        print("[3] Exit")

        choice = input("Select : ")
        if choice == "1":
            createAccount() 
        if choice == "2":
            signIn()
        if choice == "3":
            break

    else:
        name = logged_in
        while True:
            print(f"\nLogged in with the name {logged_in}")
            print("[1] Deposit")
            print("[2] Withdraw")
            print("[3] View balance")
            print("[4] Transaction history")
            print("[5] Log out")

            choice = input("Select : ")
            if choice == "1":
                
                try:
                    amount = float(input("Amount: "))
                except ValueError:
                    print("Invalid amount!")  

                users[name]["balance"] += amount
                userSave(users)
                transaction = f'Date : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Name : {name} | ID : {users[name]["card_no"]} | Status : {amount} manat loaded in the account\n'
                trSave(transaction)
            if choice == "2":
                
                try:
                    amount = float(input("Amount: "))
                except ValueError:
                    print("Invalid amount!")

                while amount > users[name]["balance"]:
                    print("Insufficient balance")
                    amount = float(input("Amount of money : "))
                else:
                    users[name]["balance"] -= amount
                    userSave(users)
                    transaction = f'Date : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Name : {name} | ID : {users[name]["card_no"]} | Status : {amount} manat withdrawn from the account\n'
                    trSave(transaction)
            if choice == "3":
                print(users[name]["balance"])
            if choice == "4":
                print(trLoad())
            if choice == "5":
                logged_in = None
                saveSession(logged_in)
                break

