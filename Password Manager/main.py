import os
import store
import get
import update
import generate


while True:
    print(""" 
Select option
1] store password
2] get password
3] update password 
4] generate password
""")

    option = input("Enter option number:\t")
    if option == "1":
        site, account, passwd = store.get_info()
        store.store_pass(site, account, passwd)
    elif option == "2":
        files = os.listdir("./password")
        get.list_sites__accounts(files)
        select = get.select_site()
        get.show_account(select)
        opt = get.select_account(select)
        get.show_passw(opt)

    elif option == "3":
        files = os.listdir("./password")
        update.list_sites__accounts(files)
        select = update.select_site()
        update.show_account(select)
        opt = update.select_account(select)
        update.show_passw(opt)

    elif option == "4":
        generate.run()
    else:
        print("Please enter appropriate option!")

    again = input("\nDo you want to continue? (y/n): ")
    if again.lower() != "y":
        break
