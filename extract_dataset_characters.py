import random
import io
import argparse
import os
import csv


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LABEL_FILE = os.path.join(SCRIPT_PATH, './basis_characters.txt')

CHOSUNG_SET_NUMBER = 588
BASE_CODE = 44032


def load_basis_character(label_file):
    character_set_list = list()
    with io.open(label_file, 'r', encoding='utf-8') as f:
        labels = f.read().splitlines()

    character_set_list.append(labels)

    return character_set_list


def extract_character_set(character_set_list):

    for i in range(0, 4):

        character_list = list()

        for j in range(0, 57):
            while True:
                index = random.randrange(0, 21) * 28
                character = chr(index + BASE_CODE + (j % 19) * CHOSUNG_SET_NUMBER)

                k = 0
                while k < len(character_set_list):
                    if character in character_set_list[k]:
                        break
                    k += 1

                if k == len(character_set_list):
                    character_list.append(character)
                    break

        for j in range(57, 114):
            while True:
                index1 = random.randrange(0, 21) * 28
                index2 = random.randrange(1, 28)
                index = (index1 + index2)
                character = chr(index + BASE_CODE + (j % 19) * CHOSUNG_SET_NUMBER)

                k = 0
                while k < len(character_set_list):
                    if character in character_set_list[k]:
                        break
                    k += 1

                if k == len(character_set_list):
                    character_list.append(character)
                    break

        character_set_list.append(character_list)

    return character_set_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--label-file', type=str, dest='label_file',
                        default=DEFAULT_LABEL_FILE,
                        help='File containing newline delimited labels.')
    args = parser.parse_args()
    character_list = load_basis_character(args.label_file)
    f = open('output.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(f)

    for unicode_list in extract_character_set(character_list):
        writer.writerow(unicode_list)

    f.close()

