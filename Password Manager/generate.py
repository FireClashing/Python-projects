import time
import os
import pyperclip
import random


def run():
    alph = list("abcdefghijklmnopqrstuvwxyz")
    cap_alph = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    num = list("1234567890")
    spec = list('~!@#$%^&*()_+{}:"<>?|][]')

    lst = []
    lst1 = []
    lst2 = []
    lst3 = []

    for i in range(random.randint(3, 10)):
        lst.append(random.choice(alph))

    for i in range(random.randint(3, 10)):
        lst1.append(random.choice(cap_alph))

    for i in range(random.randint(3, 10)):
        lst2.append(random.choice(num))

    for i in range(random.randint(3, 10)):
        lst3.append(random.choice(spec))

    pasw = lst + lst1 + lst2 + lst3
    random.shuffle(pasw)
    a = ""
    for i in range(len(pasw)):
        a += pasw[i]
    print(f"\n\nGenerated password : \t{a} \n\n")
    pyperclip.copy(a)

    print("The generated password is copied to the clipboard!")
    print("\n\n\t\t\tEXITING")
    time.sleep(5)
    os.system("clear")
