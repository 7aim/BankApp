import json

users = {}
logged_in = None

def userLoad():
    global users
    try:
        with open("accounts.json", "r", encoding="utf-8") as dosya:
            users = json.load(dosya)
    except FileNotFoundError:
        users = []  # Eğer dosya bulunmazsa boş bir liste

def userSave(data):
    with open("accounts.json", "w", encoding="utf-8") as dosya:
        json.dump(data, dosya, indent=4)

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

        #Pul yukleme/cekme
        choice = input("Select : ")
        if choice == "1":
            amount = input("Amount of money")
            balance += amount
        if choice == "2":
            amount = input("Amount of money")
            while amount > balance:
                print("Insufficient balance")
                amount = input("Amount of money")
            else:
                balance += amount
        if choice == "3":
            print(balance)
        if choice == "4":
            pass
        if choice == "5":
            logged_in = None

    if choice == "3":
        break