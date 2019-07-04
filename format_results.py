import json


def main():
    result_file = open("Results.json", 'r', encoding='utf-8')
    results = json.load(result_file)
    result_file.close()

    election_file = open("Election.csv", 'w', encoding='utf-8')
    election_file.write('Name, C/S,, T-Length,, CT/T,, Logical,, ARI,, FRE\n')
    hurricane_file = open("Hurricane.csv", 'w', encoding='utf-8')
    hurricane_file.write('Name,, C/S,, T-Length,, CT/T,, Logical,, ARI,, FRE\n')

    for senator in results:
        if 'election' in results[senator]:
            election_file.write(senator + ',' + str(round(results[senator]['non-election']['cps']['mean'], 3)) + ',' +
                                str(round(results[senator]['election']['cps']['mean'], 3)) + ',' +
                                str(round(results[senator]['non-election']['t-unit length']['mean'], 3)) + ',' +
                                str(round(results[senator]['election']['t-unit length']['mean'], 3)) + ',' +
                                str(round(results[senator]['non-election']['ctr']['mean'], 3)) + ',' +
                                str(round(results[senator]['election']['ctr']['mean'], 3)) + ',' +
                                str(round(results[senator]['non-election']['logical complexity']['mean'], 3)) + ',' +
                                str(round(results[senator]['election']['logical complexity']['mean'], 3)) + ',' +
                                str(round(results[senator]['non-election']['ari']['mean'], 3)) + ',' +
                                str(round(results[senator]['election']['ari']['mean'], 3)) + ',' +
                                str(round(results[senator]['non-election']['flesch']['mean'], 3)) + ',' +
                                str(round(results[senator]['election']['flesch']['mean'], 3)) + '\n')

        if 'hurricanes' in results[senator]:
            hurricane_file.write(senator + ',' + str(round(results[senator]['non-hurricanes']['cps']['mean'], 3)) + ',' +
                                 str(round(results[senator]['hurricanes']['cps']['mean'], 3)) + ',' +
                                 str(round(results[senator]['non-hurricanes']['t-unit length']['mean'], 3)) + ',' +
                                 str(round(results[senator]['hurricanes']['t-unit length']['mean'], 3)) + ',' +
                                 str(round(results[senator]['non-hurricanes']['ctr']['mean'], 3)) + ',' +
                                 str(round(results[senator]['hurricanes']['ctr']['mean'], 3)) + ',' +
                                 str(round(results[senator]['non-hurricanes']['logical complexity']['mean'], 3)) + ',' +
                                 str(round(results[senator]['hurricanes']['logical complexity']['mean'], 3)) + ',' +
                                 str(round(results[senator]['non-hurricanes']['ari']['mean'], 3)) + ',' +
                                 str(round(results[senator]['hurricanes']['ari']['mean'], 3)) + ',' +
                                 str(round(results[senator]['non-hurricanes']['flesch']['mean'], 3)) + ',' +
                                 str(round(results[senator]['hurricanes']['flesch']['mean'], 3)) + '\n')

    election_file.close()
    hurricane_file.close()


main()
