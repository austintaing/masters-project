import glob
import re

namelist = glob.glob("D:/Austin/Documents/Class/CongressPressExpand/*/*.txt")

out = open("text.csv","w")
errorlist=[]
for name in namelist:
    try:
        print("Reading file:", name)
        f = open(name, "r")
        text = f.read()
        f.close()
        text = text.replace('\n', ' ')
        text = text.replace('"', '""')
        re.sub(' +',' ',text)
        print(",\""+text+"\"", file=out)

    except Exception as inst:
        print("Error reading file")
        errorlist.append(name)
    
out.close()

errorlist2 = []
for name in errorlist:
    try:
        print("Reading unicode file:", name)
        f = open(name, "r", encoding='utf-8')
        text = f.read()
        f.close()
        text = text.replace('\n', ' ')
        text = text.replace('"', '""')
        re.sub(' +', ' ', text)
        print(",\""+text+"\"", file=out)
    except Exception as inst:
        errorlist2.append(name)
        print("Error reading file")

err = open("error files.txt", 'w')
for n in errorlist2:
    print(n, file=err)
err.close()
