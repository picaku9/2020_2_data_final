import csv
from requests import get
import os
import shutil

fileName ='lists.csv'

myCSVFile = open(fileName, 'r')
next(myCSVFile)
myFile =csv.reader(myCSVFile)


def download(url, file_name):
    with open(file_name, "wb") as file:   # open in binary mode
        response = get(url)               # get request
        file.write(response.content)      # write to file

'''
for row in myFile:
	print(row[0])
	url = "http://220.86.190.58:5959/"
	download(url+row[0]+".apk",row[0])

'''

pwd=os.getcwd()
    
for row in myFile:
	if row[7] == '0' :
		print(row[7])
		shutil.move(pwd+"\\"+ row[0]+".apk", pwd+"\\benign\\"+row[0]+".apk")
	else :
		shutil.move(pwd+"\\"+ row[0], pwd+"\\"+ row[0] + ".apk")

myCSVFile.close()


