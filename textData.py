import os

## Import .txt files from ./data/ into a python object
def importText(number):
    f = open('data/{}.txt'.format(number), 'rb')
    text = f.read()
    f.close()
    return text
