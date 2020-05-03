"""
Prepare flat file to be in common format that datafly can consume.
Drop all specified identity columns and use comma as delimiter.
"""


import argparse
import csv
import sys
from datetime import datetime
import numpy as np

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Prepation of flat file as input to datafly.py")
    parser.add_argument("--private_table", "-pt", required=True,
                        type=str, help="Path to the CSV table to K-anonymize.")
    parser.add_argument("--unique_identifier", "-id", required=True,
                        type=str, help="Names of the unique identifier attributes that are to be removed.",
                        nargs='+')
    parser.add_argument("--output", "-o", required=True,
                        type=str, help="Path to the output file.")
    args = parser.parse_args()

    try:
        start = datetime.now()
        lines = []

        with open(args.private_table, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            fields = next(csv_reader)
            ignored_indexes = []

            for i in range(len(fields)):
                # TODO: make this case-insensitive
                if fields[i] in args.unique_identifier:
                    ignored_indexes.append(i)

            reversed(ignored_indexes)

            lines.append(fields)

            for line in csv_reader:
                lines.append(line)

        for i in ignored_indexes:
            lines = np.delete(lines, i, axis=1)

        with open(args.output, "w", newline='') as new_csv:
            csv_writer = csv.writer(new_csv, delimiter=',')
            csv_writer.writerows(lines)

        end = (datetime.now() - start).total_seconds()
        print("[LOG] Done in %.2f seconds (%.3f minutes (%.2f hours))" % (end, end / 60, end / 60 / 60))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
