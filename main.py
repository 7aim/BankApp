#login
id = 123
name = input("Name : ")
password = input("Password : ")
card_no = input("Card Number : ")


user = {"id" : id,
        "name" : name,
        "password" : password,
        "card_no" : card_no
        }

#singin
name = input("Name : ")
if name in user["name"]:
    print("1")
else:
    print("2")

password = input("Password : ")
if password in user["password"]:
    print("1")
else:
    print("2")

card_no = input("Card Number : ")
if card_no in user["card_no"]:
    print("1")
else:
    print("2")