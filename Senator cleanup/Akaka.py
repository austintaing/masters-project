def akaka():
    in_file = open("Senators/Akaka.csv", 'r', encoding = 'utf-8')
    out_file = open("Senators/Akaka_clean.csv", 'w', encoding='utf-8')

    for line in in_file:
        parts = line.split(',', 4)
        parts[-1] = parts[-1][parts[-1].find("WASHINGTON DC"):].rstrip()
        out_line = ','.join(parts)
        out_file.write(out_line+'\n')

    in_file.close()
    out_file.close()
