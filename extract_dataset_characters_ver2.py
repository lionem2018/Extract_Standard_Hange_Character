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
        character_set_list.append(character_list)

        jungsung_index = list(range(21))
        jungsung_index += list(range(21))
        for j in range(0, 15):
            jungsung_index.append(random.randrange(0, 21))

        jongsung_index = list(range(1, 28))
        jongsung_index += list(range(1, 28))
        jongsung_index.append(random.randrange(1, 28))
        jongsung_index.append(random.randrange(1, 28))
        jongsung_index.append(random.randrange(1, 28))

        random.shuffle(jungsung_index)
        random.shuffle(jongsung_index)

        for j in range(0, 57):
            index = jungsung_index[j] * 28
            character = chr(index + BASE_CODE + (j % 19) * CHOSUNG_SET_NUMBER)

            for k in range(0, len(character_set_list)):
                if character in character_set_list[k]:
                    print(character, ": 종성X 중복")

            character_list.append(character)

        for j in range(57, 114):
            index1 = jungsung_index[j-57] * 28
            index2 = jongsung_index[j-57]
            index = index1 + index2
            character = chr(index + BASE_CODE + (j % 19) * CHOSUNG_SET_NUMBER)

            for k in range(0, len(character_set_list)):
                if character in character_set_list[k]:
                    print(character, ": 종성O 중복")

            character_list.append(character)

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

