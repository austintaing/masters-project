f = open("Landrieu.csv", 'r', encoding='utf-8')
of = open("Landrieu_clean.csv", 'w', encoding='utf-8')
for line in f:
    start = line.find("WASHINGTON")+11
    if start != 10:
        line = line[:14]+line[start:]
        of.write(line)
    
f.close()
of.close()