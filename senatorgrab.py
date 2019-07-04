import glob
import re
import time


start = time.time()


def clean_text(t):
    t.replace('"', '')
    t_list = t.split()
    t = ' '.join(t_list)
    return t


namelist = glob.glob("D:/Austin/Documents/Class/CongressPressExpand/*")

bigerrorlist = []

for senator in namelist:
    div = senator.rfind('\\')
    sen_name = senator[div+1:]

    senslist = glob.glob(senator+'/*')

    out = open("Senators/"+sen_name+".csv", "w", encoding='utf-8')
    errorlist = []
    for name in senslist:
        f = open(name, "r")
        try:
            text = f.read()
        except Exception:
            f.close()
            f = open(name, "r", encoding='utf-8')
            try:
                text = f.read()
            except Exception:
                f.close()
                f = open(name, "r", encoding='latin-1')
                try:
                    text = f.read()
                except Exception:
                    errorlist.append(name)
                    continue
        f.close()

        text = clean_text(text)
        text = text.replace('"', '""')
        re.sub('[ \t]+', ' ', text)

        div = name.rfind('\\')
        div2 = name.lower().rfind(sen_name.lower())
        date = name[div+1:div2]

        year = date[-4:]
        month = date[-7:-4]
        day = date[:-7]

        print("," + year + ',' + month + ',' + day + ",\"" + text + "\"", file=out)

    out.close()

'''
    for name in errorlist:
        try:
            print("Reading unicode file:", name)
            f = open(name, "r", encoding='utf-8')
            text = f.read().strip()
            f.close()
            text = text.replace('\n', ' ')
            text = text.replace('"', '""')
            re.sub(' +', ' ', text)
            div = name.rfind('\\')
            div2 = name.lower().rfind(sen_name.lower())
            date = name[div + 1:div2]

            year = date[-4:]
            month = date[-7:-4]
            day = date[:-7]

            print("," + year + ',' + month + ',' + day + ",\"" + text + "\"", file=out)
        except Exception as inst:
            try:
                f.close()
                print("Reading latin-1 file:", name)
                f = open(name, "r", encoding='latin-1')
                text = f.read().strip()
                f.close()
                text = text.replace('\n', ' ')
                text = text.replace('"', '""')
                re.sub(' +', ' ', text)

                div = name.rfind('\\')
                div2 = name.lower().rfind(sen_name.lower())
                date = name[div + 1:div2]

                year = date[-4:]
                month = date[-7:-4]
                day = date[:-7]

                print("," + year + ',' + month + ',' + day + ",\"" + text + "\"", file=out)
            except Exception as inst:
                bigerrorlist.append(name)
                print("Error reading file")
'''
err = open("error files.txt", 'w')
for n in errorlist:
    print(n, file=err)

err.close()
end = time.time()
print(end-start)
