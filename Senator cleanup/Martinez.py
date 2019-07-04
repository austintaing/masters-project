f = open("Martinez.csv", 'r', encoding='utf-8')
of = open("Martinez_clean.csv", 'w', encoding='utf-8')
for line in f:
    start = line.find("WASHINGTON")+11
    if start != 10:
        line = line[:14]+line[start:]
    else:
        start = line.find("200", 14)+5
        if start != 9:
            line = line[:14]+line[start:]
    of.write(line)
    
f.close()
of.close()