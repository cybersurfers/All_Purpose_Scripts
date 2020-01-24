#!/usr/bin/env python3
'''
Provided a password list, this will attempt to unlock a zip file with each password in the list.
'''

#usage:
#python3 Zip_brute_forcer.py 'filename.zip' 'passwordList.txt'

from zipfile import ZipFile
import os
import sys

directory = os.path.abspath('.')
filename = sys.argv[1]
passwordFile = sys.argv[2]
count = 0
fileLength = len(open(f'{directory}/{passwordFile}', errors='ignore').readlines())
with ZipFile(f'{directory}/{filename}') as zip:
    with open(f'{directory}/{passwordFile}', errors='ignore') as f:
        for passwrd in f.readlines():
            passwrd = passwrd.strip()
            try:
                zip.extractall(path=directory, pwd=passwrd.encode()) 
                exit(f'Success! The password is "{passwrd}"')
            except Exception:
                if count % 10000 == 0:
                    print(f'Processing: {count}/{fileLength}')
                count += 1
                
exit('Password not found in the list.')
