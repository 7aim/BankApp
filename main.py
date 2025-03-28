import random
users = {}
while True:
    print("""
    [1] Create account
    [2] Sign in
    [3] Exit
    """)
    chooice = input("Select : ")

    if chooice == "1":
        id = 1
        name = input("Name : ")
        password = input("Password : ")
        card_no = input("Card Number : ")
        balance = 0
        log = []

        users[name] = {"id" : id,'password': password,"card_no" : card_no,"balance" : balance,"log" : log}
        id += 1

    if chooice == "2":
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

        print("""
    [1] Deposit
    [2] Withdraw
    [3] View balance
    [4] Transaction history
    [5] Log out
        """)
        #Pul yukleme/cekme
        chooice = input("Deposit/Withdrawal : ")
        if chooice == "1":
            amount = input("Amount of money")
            balance += amount
        if chooice == "2":
            amount = input("Amount of money")
            while amount > balance:
                print("Insufficient balance")
                amount = input("Amount of money")
            else:
                balance += amount
        if chooice == "3":
            pass
        if chooice == "4":
            pass
        if chooice == "5":
            pass

    if chooice == "3":
        break