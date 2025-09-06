import subprocess
import os

print(""" ░██████╗████████╗░█████╗░██████╗░███████╗  ██████╗░░█████╗░░██████╗░██████╗░██╗░░░░░░░██╗░█████╗░██████╗░██████╗░
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝  ██╔══██╗██╔══██╗██╔════╝██╔════╝░██║░░██╗░░██║██╔══██╗██╔══██╗██╔══██╗
╚█████╗░░░░██║░░░██║░░██║██████╔╝█████╗░░  ██████╔╝███████║╚█████╗░╚█████╗░░╚██╗████╗██╔╝██║░░██║██████╔╝██║░░██║
░╚═══██╗░░░██║░░░██║░░██║██╔══██╗██╔══╝░░  ██╔═══╝░██╔══██║░╚═══██╗░╚═══██╗░░████╔═████║░██║░░██║██╔══██╗██║░░██║
██████╔╝░░░██║░░░╚█████╔╝██║░░██║███████╗  ██║░░░░░██║░░██║██████╔╝██████╔╝░░╚██╔╝░╚██╔╝░╚█████╔╝██║░░██║██████╔╝
╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝  ╚═╝░░░░░╚═╝░░╚═╝╚═════╝░╚═════╝░░░░╚═╝░░░╚═╝░░░╚════╝░╚═╝░░╚═╝╚═════╝░
""")


def get_info():
    site = input("Enter site or app: example.com\t")
    account = input("Enter account name:\t")
    passwd = input("Enter your password:\t")

    return site, account, passwd


def store_pass(site, account, passwd):
    if site in os.listdir(".password"):
        subprocess.run(["touch", f"{account}"], cwd=f".password/{site}")
    else:
        subprocess.run(["mkdir", f"{site}"], cwd=".password")

    subprocess.run(["touch", f"{account}"], cwd=f".password/{site}")
    with open(f".password/{site}/{account}", "w") as f:
        f.write(passwd)


def run():
    site, account, passwd = get_info()
    store_pass(site, account, passwd)
