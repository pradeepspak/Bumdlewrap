from bundlewrap.repo import Repository
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


repo = Repository(dir_path)


def generate():
    key = input("Enter the desired key: ")
    while True:
        unencrypted = input("Please enter the unencrypted PW: ")
        pw = repo.vault.encrypt(unencrypted, key=key)
        print(pw)
        pass


generate()
