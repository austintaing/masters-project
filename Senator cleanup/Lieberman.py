f = open("Lieberman.csv", 'r', encoding='utf-8')
of = open("Lieberman_clean.csv", 'w', encoding='utf-8')
for line in f:
    start = line.find("WASHINGTON")+11
    if start != 10:
        line = line[:14]+line[start:]
    else:
        start = line.find("Contact")+8
        if start != 7:
            line = line[:14]+line[start:]
    of.write(line)
    
f.close()
of.close()