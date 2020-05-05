"""
Calculate precision of the k-anonymity
https://dataprivacylab.org/dataprivacy/projects/kanonymity/kanonymity2.pdf
"""
import argparse
import csv
from datetime import datetime


def load_csv(file_path):
    lines = []

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            lines.append(line)

    return lines


def calculate_precision(csv_data, qi_indexes, vghs):
    p = 0

    for row in csv_data:
        for i, qi_index in enumerate(qi_indexes):
            data = row[qi_index]
            vgh = vghs[i]
            p += get_avg_level(data, vgh)

    p = 1 - (p / (len(csv_data) * len(qi_indexes)))

    return p


def get_avg_level(data, vgh):
    depth = len(vgh[0])
    level = 0
    found = False

    for row in vgh:
        for c in range(len(row)):
            if row[c] == data:
                level = c
                found = True
                break

        if found:
            break

    return level / depth


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Python implementation to calculate the precision of k-anonymous data.")
    parser.add_argument("--private_table", "-pt", required=True,
                        type=str, help="Path to the K-anonymized csv table.")
    parser.add_argument("--quasi_identifier", "-qi", required=True,
                        type=str, help="Index of the attributes which are Quasi Identifiers, starting from 0 "
                                       "of the private table.",
                        nargs='+')
    parser.add_argument("--domain_gen_hierarchies", "-dgh", required=True,
                        type=str, help="Paths to the generalization files (must have same order as "
                                       "the QI index list.",
                        nargs='+')
    args = parser.parse_args()

    try:
        start = datetime.now()

        if len(args.quasi_identifier) != len(args.domain_gen_hierarchies):
            raise Exception("Parameters' dimensions mismatch")

        qi_idx = [int(i) for i in args.quasi_identifier]
        gen_data = []

        for i, dgh_path in enumerate(args.domain_gen_hierarchies):
            gen_data += [load_csv(dgh_path)]

        anon_file = load_csv(args.private_table)

        precision = calculate_precision(anon_file, qi_idx, gen_data)
        print('[LOG] Precision = {0:.16f}'.format(precision))

        end = (datetime.now() - start).total_seconds()

        print("[LOG] Done in %.2f seconds (%.3f minutes (%.2f hours))" %
              (end, end / 60, end / 60 / 60))

    except FileNotFoundError as error:
        print("[ERROR] File '%s' has not been found." % error.filename)
    except IOError as error:
        print("[ERROR] There has been an error with reading file '%s'." % error.filename)
