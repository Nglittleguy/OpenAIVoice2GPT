import os
import csv

## Import .txt files from ./data/ into a python object
def importText(number):
    f = open('data/{}.txt'.format(number), 'rb')
    text = f.read()
    f.close()
    return text

## Import .csv files from ./data/stay.csv into a python object
def getCustomerInfo(customerId):
    f = csv.reader(open('data/stay.csv', "r"), delimiter=",")

    #loop through the csv list
    for customer in f:
        #if current rows 2nd value is equal to input, print that row
        if customerId == customer[0]:
            return customer
        
    return 0