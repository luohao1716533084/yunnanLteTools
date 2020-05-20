#coding:utf-8

import os

path = os.getcwd()
dirs = os.listdir(path)
file_file = ['', '']
for i in dirs:
    if "EUtranCellTDD" in i:
        file_file[0] = i
    if "EUtranReselectionTDD" in i:
        file_file[1] = i

print(file_file)
