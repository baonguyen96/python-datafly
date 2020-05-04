"""
Calculate precision of the k-anonymity
https://dataprivacylab.org/dataprivacy/projects/kanonymity/kanonymity2.pdf
TODO: turn into CLI tool
"""
import csv


def load_csv(file_path):
    lines = []

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            lines.append(line)

    return lines


def calculate_precision(csv_data, age_index, education_index, age_vgh, edu_vgh):
    p = 0

    # knowing na is 2 since 2 qi indexes

    for row in csv_data:
        age = row[age_index]
        edu = row[education_index]
        p += get_avg_level(age, age_vgh) + get_avg_level(edu, edu_vgh)

    p = 1 - (p / (len(csv_data) * 2))

    return p


def get_avg_level(data, vgh):
    depth = len(vgh[0])
    level = 0

    for row in vgh:
        for c in range(len(row)):
            if row[c] == data:
                level = c
                break

    return level / depth


main_path = ".\\HW\\HW4\\data\\"
age_gen = load_csv(main_path + "age_generalization.csv")
education_gen = load_csv(main_path + "education_generalization.csv")
anon_file = load_csv(main_path + "adult_no_ssn.csv")

precision = calculate_precision(anon_file, 0, 3, age_gen, education_gen)
print(precision)
