import random
users = {}
while True:
    chooice = input("1/2 : ")
    if chooice == "1":
        #login
        id = 1
        name = input("Name : ")
        password = input("Password : ")
        card_no = input("Card Number : ")
        balance = 0
        log = []

        users[name] = {"id" : id,'password': password,"card_no" : card_no,"balance" : balance,"log" : log}
        id += 1
        print(users)

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