import json
import datetime
import hashlib

users = {}
logged_in = None

def hashPassword(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Tranzaksiya 
def trLoad():
    with open("db/transaction.txt", 'r') as f:
        return f.read()

def trSave(tr_data):
    with open("db/transaction.txt", 'a') as f:
        f.write(tr_data)

# Hesablar
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

# Yadda qalan giris
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
    while len(card_no) != 4:
        print("Card no must be 4 digits")
        card_no = input("Card Number : ")

    user_card_no = []
    for i in users:
        user_card_no.append(users[i]["card_no"])

    while card_no in user_card_no:
        print("This card no already exists")
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
            print("[3] Send money")
            print("[4] View balance")
            print("[5] Transaction history")
            print("[6] Log out")

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
                    amount = float(input("Amount : "))
                else:
                    users[name]["balance"] -= amount
                    userSave(users)
                    transaction = f'Date : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Name : {name} | ID : {users[name]["card_no"]} | Status : {amount} manat withdrawn from the account\n'
                    trSave(transaction)
            if choice == "3":
                card_no = input("Card no : ")
                cardHave = False
                for i in users:
                    if users[i]["card_no"] == card_no:
                        print(f"Is this the person you want to send money to? {i}")
                        choice = input("Yes [1] | No [2] : ")
                        if choice == "1":

                            try:
                                amount = float(input("Amount: "))
                            except ValueError:
                                print("Invalid amount!")
                                break

                            while amount > users[name]["balance"]:
                                print(f"Insufficient balance.Your balance : {users[name]["balance"]}")
                                choice = input("Continue [1] | Go back [2] : ")
                                if choice == "1":                                    
                                    amount = float(input("Amount : "))
                                else:
                                    break

                            users[logged_in]["balance"] -= amount
                            users[i]["balance"] += amount
                            userSave(users)
                            cardHave = True

                            if cardHave is True:
                                print("Process successful : Money sent.")
                            else:
                                print("Process unsuccessful : Card no not found.")

                        if choice == "2":
                            print("Process unsuccessful")


            if choice == "4":
                print(f"Your balance : {users[name]["balance"]}")
            if choice == "5":
                print(trLoad())
            if choice == "6":
                logged_in = None
                saveSession(logged_in)
                break

