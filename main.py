import json
import datetime

users = {}
logged_in = None
             
def trSave(log_data):
    with open("transaction.txt", 'a') as f:
        f.write(log_data)

def userLoad():
    global users
    try:
        with open("accounts.json", "r", encoding="utf-8") as f:
            users = json.load(f)
    except:
        users = {}

def userSave(data):
    with open("accounts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def createAccount():
    id = 1
    name = input("Name : ")
    password = input("Password : ")
    card_no = input("Card Number : ")
    balance = 0
    log = []

    users[name] = {"id" : id,'password': password,"card_no" : card_no,"balance" : balance,"log" : log}
    userSave(users)
    id += 1

def singIn():
    global logged_in
    global name

    name = input("Name : ")
    for i in users:     
        while name not in users:
            print("False")
            name = input("Name : ")

    password = input("Password : ")
    while password not in users[name]["password"]:
        print("False")
        password = input("Password : ")

    card_no = input("Card Number : ")
    while card_no not in users[name]["card_no"]:
        print("False")
        card_no = input("Card Number : ")
    print("True")
    logged_in = name

while True:
    userLoad()

    print("[1] Create account")
    print("[2] Sign in")
    print("[3] Exit")

    choice = input("Select : ")

    if choice == "1":
        createAccount()

    if choice == "2":
        singIn()
        
        print("[1] Deposit")
        print("[2] Withdraw")
        print("[3] View balance")
        print("[4] Transaction history")
        print("[5] Log out")

        choice = input("Select : ")
        if choice == "1":
            amount = float(input("Amount of money : "))       
            users[name]["balance"] += amount
            userSave(users)
            transaction = f'Date : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Name:{name} | ID : {users[name]["card_no"]} | Status : {amount} manat loaded in the account\n'
            trSave(transaction)
        if choice == "2":
            amount = input("Amount of money")
            while amount > users[name]["balance"]:
                print("Insufficient balance")
                amount = input("Amount of money")
            else:
                users[name]["balance"] -= amount
                transaction = f'Date : {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Name : {name} | ID : {users[name]["card_no"]} | Status : {amount} manat withdrawn from the account\n'
                trSave(transaction)
        if choice == "3":
            print(users[name]["balance"])
        if choice == "4":
            pass
        if choice == "5":
            logged_in = None

    if choice == "3":
        break