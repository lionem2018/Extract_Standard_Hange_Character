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


def check_and_replace_no_jongsung_character(character_index, character, character_set_list, jungsung_index_list):
    for k in range(0, len(character_set_list)):
        if character in character_set_list[k]:

            new_index = -1
            while new_index not in jungsung_index_list[character_index:]:
                new_index = random.randrange(0, 21)

            jungsung_list_index = jungsung_index_list[character_index:].index(new_index)
            jungsung_index_list[character_index], jungsung_index_list[jungsung_list_index] = jungsung_index_list[jungsung_list_index], \
                                                                     jungsung_index_list[character_index]

            index = jungsung_index_list[character_index] * 28
            character = chr(index + BASE_CODE + (character_index % 19) * CHOSUNG_SET_NUMBER)
            print(character)
            character = check_and_replace_no_jongsung_character(character_index, character, character_set_list, jungsung_index_list)
            return character
    return character


def check_and_replace_character(character_index, character, character_set_list, jungsung_index_list, jongsung_index_list):
    for k in range(0, len(character_set_list)):
        if character in character_set_list[k]:

            new_index1 = -1
            while new_index1 not in jungsung_index_list[character_index:]:
                new_index1 = random.randrange(0, 21)

            new_index2 = -1
            while new_index2 not in jongsung_index_list[character_index:]:
                new_index2 = random.randrange(1, 28)

            jungsung_list_index = jungsung_index_list[character_index:].index(new_index1)
            jungsung_index_list[character_index], jungsung_index_list[jungsung_list_index] = jungsung_index_list[jungsung_list_index], \
                                                                     jungsung_index_list[character_index]

            jongsung_list_index = jongsung_index_list[character_index:].index(new_index2)
            jongsung_index_list[character_index], jongsung_index_list[jongsung_list_index] = jongsung_index_list[jongsung_list_index], \
                                                                     jongsung_index_list[character_index]

            index = jungsung_index_list[character_index] * 28 + jongsung_index_list[character_index]
            character = chr(index + BASE_CODE + (character_index % 19) * CHOSUNG_SET_NUMBER)
            print(character)
            character = check_and_replace_character(character_index, character, character_set_list, jungsung_index_list, jongsung_index_list)
            return character

    return character


def extract_character_set(character_set_list, set_num):

    for i in range(len(character_set_list), set_num):

        character_list = list()
        character_set_list.append(character_list)

        jungsung_index_list = list(range(21))
        jungsung_index_list += list(range(21))
        for j in range(0, 15):
            jungsung_index_list.append(random.randrange(0, 21))

        jongsung_index_list = list(range(1, 28))
        jongsung_index_list += list(range(1, 28))
        jongsung_index_list.append(random.randrange(1, 28))
        jongsung_index_list.append(random.randrange(1, 28))
        jongsung_index_list.append(random.randrange(1, 28))

        random.shuffle(jungsung_index_list)
        random.shuffle(jongsung_index_list)

        for j in range(0, 57):
            index = jungsung_index_list[j] * 28
            character = chr(index + BASE_CODE + (j % 19) * CHOSUNG_SET_NUMBER)

            character = check_and_replace_no_jongsung_character(j, character, character_set_list, jungsung_index_list)

            character_list.append(character)

        for j in range(57, 114):
            index1 = jungsung_index_list[j-57] * 28
            index2 = jongsung_index_list[j-57]
            index = index1 + index2
            character = chr(index + BASE_CODE + (j % 19) * CHOSUNG_SET_NUMBER)

            character = check_and_replace_character(j-57, character, character_set_list, jungsung_index_list, jongsung_index_list)

            character_list.append(character)

        print(character_list)

    return character_set_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--label-file', type=str, dest='label_file',
                        default=DEFAULT_LABEL_FILE,
                        help='File containing newline delimited labels.')
    parser.add_argument('--set-num', type=int, dest='set_num',
                        default=5,
                        help='The number of character set(one set = 114 characters)')
    parser.add_argument('--no-basis', type=int, dest='is_no_basis',
                        default=0,
                        help='If you don\'t have basis characters, It makes basis characters (defulat is 0)')

    args = parser.parse_args()

    character_list = list()
    if args.is_no_basis == 0:
        character_list = load_basis_character(args.label_file)

    f = open('output.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(f)

    for unicode_list in extract_character_set(character_list, args.set_num):
        writer.writerow(unicode_list)

    f.close()

