# UI stuff
import random
import os

import art


def clear():
    # for windows 
    if os.name == 'nt':
        os.system('cls')
        # for mac and linux(here, os.name is 'posix')
    else:
        os.system('clear')


def splash(version):
    clear()
    r = random.randint(0, 1)
    fonts = ["speed", "funfaces"]
    art.tprint("EXNERATOR", font=fonts[r])
    print("---------------")
    print("Exnerator v", version)
    print("---------------\n")


def ask(question):
    while "Invalid response!":
        reply = str(input(question + ' (y/n): ')).lower().strip()
        if reply == 'y':
            return True
        if reply == 'n':
            return False
        else:
            pass


def menu(prompt, responses):
    print(prompt)
    r = 1
    v = []
    for response in responses:
        print(r, ". ", response, sep='')
        v.append(r)
        r += 1
    while "Invalid response!":
        reply = str(input('Enter option [' + str(min(v)) + '-' + str(max(v)) + ', q to quit] : ')).strip()
        if reply.isdigit() and int(reply) in v:
            return int(reply)
        elif reply == "q":
            return 0


def chooseFile(message):
    if message != None:
        print(message)
    while True:
        filename = input("Enter a filename: ")
        if os.path.isfile(filename):
            if filename.endswith(".xlsx"):
                return filename
            else:
                print("File must be .xlsx format!")
        else:
            print("File not found!")
