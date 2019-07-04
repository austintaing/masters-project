f = open("Shelby.csv", 'r', encoding='utf-8')
of = open("Shelby_clean.csv", 'w', encoding='utf-8')
for line in f:
    start = line.find("Washington D C")+15
    if start == 14:
        start = line.find("WASHINGTON D C")+15
        if start == 14:
            start = line.find("WASHINGTON DC")+14
    if start != 14 and start != 13:
        line = line[:14]+line[start:]
    else:
        start = line.find("200", 14)+5
        if start != 9:
            line = line[:14]+line[start:]
    of.write(line)
    
f.close()
of.close()