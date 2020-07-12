import sys
import json
import base64
from os import system
from getpass import getpass

from cryptography.fernet import Fernet


def read(passwords: dict, meta_password: str):
    key = input("Select key:\n")
    if key in passwords:
        try:
            pwd = Fernet(meta_password).decrypt(str.encode(passwords[key]))
            print(pwd.decode() + '\n')
        except ValueError:
            print("Wrong meta password!\n")
    else:
        print("Wrong key!\n")


def write(passwords: dict, meta_password: str):
    key = input("Select key:\n")
    new_password = getpass("New password for " + key + '\n')
    try:
        f = Fernet(meta_password)
        new_password = f.encrypt(str.encode(new_password)).decode()
    except ValueError:
        print("Wrong meta password!\n")
        return False
    if key in passwords:
        print("Old: " + passwords[key])
    passwords[key] = new_password
    print("New: " + passwords[key] + '\n')
    return passwords


if __name__ == "__main__":
    try:
        meta_password = getpass("Write meta password:\n")
        meta_password = base64.urlsafe_b64encode(str.encode(meta_password))
        system('clear')
        with open(sys.argv[1], 'r+') as pwds:
            passwords = json.load(pwds)
            backup = passwords.copy()
            while True:
                ans = input("Read or write password? r/w/exit\n")
                if ans == 'r':
                    system('clear')
                    read(passwords, meta_password)
                elif ans == 'w':
                    system('clear')
                    passwords = write(passwords, meta_password)
                    if passwords is not False:
                        pwds.seek(0)
                        try:
                            passwords = dict(sorted(passwords.items()))
                            pwds.write(json.dumps(passwords, indent=2))
                        except IOError:
                            print("Incorrect data")
                            pwds.write(json.dumps(backup, indent=2))
                elif ans == 'exit':
                    system('clear')
                    break
    except KeyboardInterrupt:
        print("\nInterrupted")
