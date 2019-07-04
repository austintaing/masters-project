# Austin Taing
import spacy
import spacy.symbols
import textacy
import textacy.text_stats as ts
import json
import time
import math
import glob
import sys
from nltk.parse import CoreNLPParser

start = time.time()
nlp = spacy.load('en_core_web_sm')
parser = CoreNLPParser(url='http://localhost:9000')

and_list = ['and', 'with', 'including', 'also', 'plus', 'furthermore', 'additionally']
or_list = ['or', 'either', 'other', 'else', 'otherwise']
not_list = ['n\'t', 'not', 'but', 'without', 'excluding']


def flesch(doc):
    doc_stats = ts.TextStats(doc)
    return 206.835 - (1.015 * doc_stats.n_words / doc_stats.n_sents) - (
                84.6 * doc_stats.n_syllables / doc_stats.n_words)


def ari(doc):
    doc_stats = ts.TextStats(doc)
    return (0.4 * doc_stats.n_words / doc_stats.n_sents) + (6 * doc_stats.n_chars / doc_stats.n_words) - 27.4


def count_complex(tree, parent):
    n = 0
    if tree.label() in ['S', 'SQ', 'SINV', 'SBARQ'] and parent == 'SBAR':
        n += 1
    for leaf in tree:
        if type(leaf) != str:
            n += count_complex(leaf, tree.label())

    return n


def count_clauses(tree, path):
    n = 0
    try:
        if tree.label() in ['MD', 'VBD', 'VBP', 'VBZ']:
            if path[-1] == 'VP':
                if path[-2] in ['S', 'SQ', 'SINV']:
                    n += 1
    except IndexError:  # if we get here, that means the path isn't long enough to do all the tests yet
        n  # no need to do anything though

    new_path = []
    for entry in path:
        new_path.append(entry)
    new_path.append(tree.label())

    for leaf in tree:
        if type(leaf) != str:
            n += count_clauses(leaf, new_path)
    return n


def count_t(tree, path, siblings):
    n = 0
    c = 0
    is_t_root = False
    if type(tree) == str:
        siblings.remove(tree)
    else:
        siblings.remove(tree.label())

    children = []
    for leaf in tree:
        if type(leaf) != str:
            children.append(leaf.label())
        else:
            children.append(leaf)

    try:
        if tree.label() in ['S', 'SQ', 'SINV', 'SBARQ'] and 'VP' in children:
            if path[-1] == 'ROOT':
                n += 1
                is_t_root = True
            if any(x in ['S', 'SQ', 'SINV'] for x in siblings):
                if 'SBAR' not in path and 'VP' not in path:
                    n += 1
                    is_t_root = True
    except IndexError:  # if we get here, that means the path isn't long enough to do all the tests yet
        print()  # no need to do anything though

    new_path = []
    for entry in path:
        new_path.append(entry)
    new_path.append(tree.label())
    siblings.append(tree.label())

    for leaf in tree:
        if type(leaf) != str:
            r = count_t(leaf, new_path, children)
            n += r[0]
            if is_t_root:
                if count_complex(leaf, tree.label()) > 0:
                    c = 1
            else:
                c += r[1]
    return [n, c]


def count_logic_ops(tree, path):
    ands = 0
    ors = 0
    nots = 0
    if tree.label() in ['RB', 'CC'] or 'PP' in path:
        for leaf in tree:
            if type(leaf) == str:
                if leaf in and_list:
                    ands += 1
                if leaf in or_list:
                    ors += 1
                if leaf in not_list:
                    nots += 1

    new_path = []
    for entry in path:
        new_path.append(entry)
    new_path.append(tree.label())

    for leaf in tree:
        if type(leaf) != str:
            ops = count_logic_ops(leaf, new_path)
            ands += ops[0]
            ors += ops[1]
            nots += ops[2]

    return [ands, ors, nots]


def syntactic(doc):
    t_units = 0
    t_length = len(doc)
    complex_t = 0
    n_sents = 0
    n_clauses = 0
    for sent in doc.sents:
        n_sents += 1
        sent_nlp = parser.raw_parse(sent.text)
        for item in sent_nlp:
            n_clauses += count_clauses(item, [])
            t_info = count_t(item, '', ['ROOT'])
            t_units += t_info[0]
            complex_t += t_info[1]

    t_length /= t_units
    return {'sentences': n_sents, 'clauses': n_clauses, 't-units': t_units, 't-unit length': t_length,
            'complex t-units': complex_t}


def logical(doc):
    ands = 0
    ors = 0
    nots = 0
    for sent in doc.sents:
        sent_nlp = parser.raw_parse(sent.text)
        for item in sent_nlp:
            ops = count_logic_ops(item, [])
            ands += ops[0]
            ors += ops[1]
            nots += ops[2]

    return [ands, ors, nots]


def load(senator):
    f_name = "Senators/" + senator + ".csv"
    in_file = open(f_name, 'r', encoding='utf-8')
    data = []
    for line in in_file:
        meta = line.split(',', 4)
        content = textacy.preprocess.normalize_whitespace(meta[-1])
        metadata = {
            "category": meta[0],
            "year": meta[1],
            "month": meta[2],
            "day": meta[3]
        }
        doc = textacy.Doc(content, metadata=metadata, lang="en")
        data.append(doc)

    in_file.close()

    return data


hurricane_words = ['Charley', 'Dennis', 'Frances', 'Gaston', 'Ivan', 'Jeanne', 'Katrina', 'Rita', 'Wilma', 'hurricane']


def run_experiment(election_senators, hurricane_senators):
    big_data = {}
    senators_to_process = sorted(list(set(election_senators) | set(hurricane_senators)))

    for senator in senators_to_process:
        sen_file = "Senators/" + senator + ".csv"
        in_file = open(sen_file, 'r', encoding='utf-8')
        data = {}
        if senator in election_senators:
            data["election"] = []
            data["non-election"] = []
        if senator in hurricane_senators:
            data["hurricanes"] = []
            data["non-hurricanes"] = []
        for line in in_file:
            meta = line.split(',', 4)
            content = textacy.preprocess.normalize_whitespace(meta[-1])
            metadata = {
                "category": meta[0],
                "year": int(meta[1]),
                "month": meta[2],
                "day": int(meta[3])
            }
            try:
                nlp_content = nlp(content)
                doc = textacy.Doc(content, metadata=metadata, lang="en")

                doc_info = syntactic(nlp_content)
                logical_info = logical(nlp_content)
                doc_info["logical complexity"] = sum(logical_info) / doc_info['t-units']
                doc_info['flesch'] = flesch(doc)
                doc_info['ari'] = ari(doc)
                doc_info['metadata'] = metadata

                if any(x in content for x in hurricane_words):
                    metadata["category"] = "1"

                if senator in election_senators:
                    if metadata["year"] == 2006 and metadata["month"] not in ["Nov", "Dec"]:
                        data["election"].append(doc_info)
                    else:
                        data["non-election"].append(doc_info)
                if senator in hurricane_senators:
                    if metadata["category"] == '1':
                        data["hurricanes"].append(doc_info)
                    else:
                        data["non-hurricanes"].append(doc_info)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                print("Metadata:", metadata)

        in_file.close()

        result_file = open("Senator Results/" + senator + ".json", 'w', encoding='utf-8')
        json.dump(data, result_file, indent='\t', sort_keys=True)
        result_file.close()

        print("\nRead", senator)
        big_data[senator] = data

    return big_data


def process_results(results):
    summary_statistics = {}
    for senator in results:
        summary_statistics[senator] = {}
        for category in results[senator]:
            result = {'sentences': {'mean': 0, 'stdev': 0}, 'clauses': {'mean': 0, 'stdev': 0},
                      't-units': {'mean': 0, 'stdev': 0}, 'complex t-units': {'mean': 0, 'stdev': 0},
                      't-unit length': {'mean': 0, 'stdev': 0}, 'logical complexity': {'mean': 0, 'stdev': 0},
                      'flesch': {'mean': 0, 'stdev': 0}, 'ari': {'mean': 0, 'stdev': 0},
                      'cps': {'mean': 0, 'stdev': 0}, 'ctr': {'mean': 0, 'stdev': 0}}

            # accumulate totals for each measure
            for article in results[senator][category]:
                for measure in result:
                    if measure in article:
                        result[measure]['mean'] += article[measure]
                article['cps'] = article['clauses'] / article['sentences']
                result['cps']['mean'] += article['cps']
                article['ctr'] = article['complex t-units'] / article['t-units']
                result['ctr']['mean'] += article['ctr']

            # divide by number of articles to actually get the mean
            for measure in result:
                result[measure]['mean'] /= len(results[senator][category])

            # get standard deviation
            for article in results[senator][category]:
                for measure in result:
                    result[measure]['stdev'] += (result[measure]['mean'] - article[measure]) ** 2
            for measure in result:
                result[measure]['stdev'] /= len(results[senator][category])
                # noinspection PyTypeChecker
                result[measure]['stdev'] = math.sqrt(result[measure]['stdev'])

            summary_statistics[senator][category] = result

    return summary_statistics


def main():
    # election list
    # ["Akaka", "Allen", "BenNelson", "BillNelson", "Bingaman", "Burns", "Byrd", "Cantwell", "Carper", "Chafee",
    # "Clinton", "Dayton", "Dewine", "Ensign", "Feinstein", "Frist", "Hatch", "Hutchison", "Jeffords", "Kohl",
    # "Kyl", "Lieberman", "Lott", "Lugar", "Menendez", "Santorum", "Sarbanes", "Snowe", "Stabenow", "Talent", "Thomas"]

    # coastal list
    # ['BillNelson', 'Burr', 'Chambliss', 'Cochran', 'Cornyn', 'Demint', 'Graham', 'Isakson', 'Landrieu', 'Lott',
    # 'Martinez', 'Sessions', 'Shelby', 'Vitter']

    # results = run_experiment(election_senators, hurricane_senators)
    results = {}
    prev_results = glob.glob("Senator Results/*")
    for senator in prev_results:
        senator_name = senator[senator.rfind('\\')+1:-5]
        if senator_name not in results:
            prev_file = open(senator, 'r', encoding='utf-8')
            results[senator_name] = json.load(prev_file)
            prev_file.close()

    result_file = open("Raw Results.json", 'w', encoding='utf-8')
    json.dump(results, result_file, indent='\t', sort_keys=True)
    result_file.close()
    # previous_results = open("Raw Results.json", 'r', encoding='utf-8')
    # results = json.load(previous_results)
    # previous_results.close()

    end_result = process_results(results)
    result_file = open("Results.json", 'w', encoding='utf-8')
    json.dump(end_result, result_file, indent='\t', sort_keys=True)
    result_file.close()


main()
end = time.time()
print(end - start)
