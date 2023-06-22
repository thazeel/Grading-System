import os
import time
import pwinput


def clrscr():
    clear = lambda: os.system("cls")
    clear()


password = ""
# Loop Statement to Show Login Page until Password is right
while password != '1483':
    clrscr()
    print("  WELCOME\n===========\n\nUser : Administrator")
    password = pwinput.pwinput(prompt="Password : ")
    print(password)
    if password != '1483':
        print("\nWrong Password, Try Again")
    else:
        print("\nLogin Successful\nLoading Site...")
    time.sleep(3)

clrscr()
print("Main Site")
# Add Grading Codes Here
