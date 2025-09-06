import os


cwd = ".password"
files = os.listdir(cwd)
account = []
"------------------------------------------------"
"-------------------------------------CODE"


def list_sites__accounts(files):
    print("Sites and apps           accounts\n-----------------------------------")
    for i in range(len(files)):
        print(f"{i + 1}  {files[i]}  \t\t    {len(os.listdir(cwd + '/' + files[i]))}")

    print("-----------------------------------")


def select_site():
    while True:
        try:
            select = int(input("Enter option to select:\t"))
            if select <= len(files):
                break
            else:
                print("Please select appropriate option")
        except ValueError:
            print("Please select only numerical value")
    os.system("clear")
    return select - 1


def show_account(select):
    print(f"----------{files[select]}----------")
    global account
    account = os.listdir(f"{cwd}/{files[select]}")
    for i in range(len(account)):
        print(f"{i + 1}   {account[i]}")


def select_account(select):
    while True:
        try:
            opt = int(input("Enter option to select:\t"))
            if opt <= len(os.listdir(f"{cwd}/{files[select]}")):
                break

            else:
                print("Please select appropriate option!")
        except ValueError:
            print("Please select numerical value ")
    os.system("clear")
    return opt - 1


def show_passw(opt):
    update = input("Enter your new password:\t")
    with open(f"{cwd}/{files[select]}/{account[opt]}", "w") as f:
        f.write(update)


"---------------------------------------------"
"--------------------Run Functions"


def run():
    list_sites__accounts(files)
    select = select_site()
    show_account(select)
    opt = select_account(select)
    show_passw(opt)
