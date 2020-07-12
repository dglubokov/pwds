import sys
import json
import base64
from cryptography.fernet import Fernet


def read(passwords: dict, meta_password: str):
    key = input("Select key:\n")
    if key in passwords:
        try:
            pwd = Fernet(meta_password).decrypt(str.encode(passwords[key]))
            print(pwd.decode() + '\n')
        except:
            print("Wrong meta password!\n")
    else:
        print("Wrong key!\n")


def write(passwords: dict, meta_password: str):
    key = input("Select key:\n")
    new_password = input("New password for " + key + '\n')
    if key in passwords:
        print("Old: ", passwords[key])
    f = Fernet(meta_password)
    new_password = f.encrypt(str.encode(new_password)).decode()
    passwords[key] = new_password
    print("New: " + passwords[key] + '\n')
    return passwords
    

if __name__ == "__main__":
    meta_password =  base64.urlsafe_b64encode(str.encode(sys.argv[2]))
    with open(sys.argv[1], 'r') as pwds:
        passwords = json.load(pwds)
    with open(sys.argv[1], 'w') as pwds:
        pass
    while True:
        ans = input("Read or write password? r/w/exit\n")
        if ans == 'r':
            read(passwords, meta_password)
        elif ans == 'w':
            passwords = write(passwords, meta_password)
        elif ans == 'exit':
            with open(sys.argv[1], 'w') as pwds:
                pwds.write(json.dumps(passwords))
            break