import random
import io
import argparse
import os


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LABEL_FILE = os.path.join(SCRIPT_PATH, './basis_characters.txt')

CHOSUNG_SET_NUMBER = 588
BASE_CODE = 44032


def load_basis_character(label_file):
    character_list = list()
    with io.open(label_file, 'r', encoding='utf-8') as f:
        labels = f.read().splitlines()

        for label in labels:
            character_list.append(ord(label))

    return character_list


def extract_character_set(character_list):

    for i in range(0, 4):

        for j in range(0, 57):
            while True:
                index = random.randrange(0, 21) * 28
                character = index + BASE_CODE + (j%19) * CHOSUNG_SET_NUMBER

                if character not in character_list:
                    character_list.append(character)
                    break

        for j in range(57, 114):
            while True:
                index1 = random.randrange(0, 21) * 28
                index2 = random.randrange(1, 28)
                index = (index1 + index2)
                character = index + BASE_CODE + (j % 19) * CHOSUNG_SET_NUMBER

                if character not in character_list:
                    character_list.append(character)
                    break

    return character_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--label-file', type=str, dest='label_file',
                        default=DEFAULT_LABEL_FILE,
                        help='File containing newline delimited labels.')
    args = parser.parse_args()
    character_list = load_basis_character(args.label_file)
    for unicode in extract_character_set(character_list):
        print(unicode, chr(unicode))
