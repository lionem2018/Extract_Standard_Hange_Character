import io
import os
import argparse
import copy


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

# Default data paths.
DEFAULT_LABEL_FILE = os.path.join(SCRIPT_PATH, './2350-common-hangul.txt')
DEFAULT_OUTPUT_DIR = os.path.join(SCRIPT_PATH, './output')

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ',
                'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ',
                 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

JUNGSUNG_CASE = [['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅣ'],
                 ['ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ'],
                 ['ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ']]

# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ',
                 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

BASE_CODE = 44032
CHOSUNG_SET_NUMBER = 588
JUNGSUNG_NUMBER = 28


def read_character_file(label_file):

    with io.open(label_file, 'r', encoding='utf-8') as f:
        labels = f.read().splitlines()

    return labels


def detach_character(character):
    """
    초성 중성 종성 분리 하기
    유니코드 한글은 0xAC00 으로부터
    초성 19개, 중성21개, 종성28개로 이루어지고
    이들을 조합한 11,172개의 문자를 갖는다.

    한글코드의 값 = ((초성 * 21) + 중성) * 28 + 종성 + 0xAC00
    (0xAC00은 'ㄱ'의 코드값)

    따라서 다음과 같은 계산 식이 구해진다.
    유니코드 한글 문자 코드 값이 X일 때,

    초성 = ((X - 0xAC00) / 28) / 21
    중성 = ((X - 0xAC00) / 28) % 21
    종성 = (X - 0xAC00) % 28

    이 때 초성, 중성, 종성의 값은 각 소리 글자의 코드값이 아니라
    이들이 각각 몇 번째 문자인가를 나타내기 때문에 다음과 같이 다시 처리한다.

    초성문자코드 = 초성 + 0x1100 //('ㄱ')
    중성문자코드 = 중성 + 0x1161 // ('ㅏ')
    종성문자코드 = 종성 + 0x11A8 - 1 // (종성이 없는 경우가 있으므로 1을 뺌)

    """

    result = list()
    char_code = ord(character) - BASE_CODE
    char1 = int(char_code / CHOSUNG_SET_NUMBER)
    result.append(CHOSUNG_LIST[char1])
    char2 = int((char_code - (CHOSUNG_SET_NUMBER * char1)) / JUNGSUNG_NUMBER)
    result.append(JUNGSUNG_LIST[char2])
    char3 = int((char_code - (CHOSUNG_SET_NUMBER * char1) - (JUNGSUNG_NUMBER * char2)))
    result.append(JONGSUNG_LIST[char3])

    return result


# def count_case_number(case_list):
#
#     pre_char1 = ' '
#     count = 0
#
#     for character in case_list:
#         char_code = ord(character) - BASE_CODE
#         char1 = int(char_code / CHOSUNG_SET_NUMBER)
#
#         if pre_char1 != char1:
#             count += 1
#             pre_char1 = char1
#
#     return count


def classify_case(labels):

    jongsung_count = list()
    jungsung_count = list()
    case = list()

    for i in range(0, 6):
        case.append([])

    for i in range(0, 19):
        for j in range(0, 6):
                case[j].append([])

    for i in range(0, 28):
        jongsung_count.append(0)

    for i in range(0, 21):
        jungsung_count.append(0)

    for character in labels:
        char_elements = detach_character(character)
        if char_elements[2] == JONGSUNG_LIST[0]:
            if char_elements[1] in JUNGSUNG_CASE[0]:
                case[0][CHOSUNG_LIST.index(char_elements[0])].insert(JUNGSUNG_CASE[0].index(char_elements[1]), character)
            elif char_elements[1] in JUNGSUNG_CASE[1]:
                case[1][CHOSUNG_LIST.index(char_elements[0])].insert(JUNGSUNG_CASE[1].index(char_elements[1]), character)
            else:
                case[2][CHOSUNG_LIST.index(char_elements[0])].insert(JUNGSUNG_CASE[2].index(char_elements[1]), character)
        else:
            if char_elements[1] in JUNGSUNG_CASE[0]:
                case[3][CHOSUNG_LIST.index(char_elements[0])].append(character)
            elif char_elements[1] in JUNGSUNG_CASE[1]:
                case[4][CHOSUNG_LIST.index(char_elements[0])].append(character)
            else:
                case[5][CHOSUNG_LIST.index(char_elements[0])].append(character)

        jongsung_count[JONGSUNG_LIST.index(char_elements[2])] += 1

        if char_elements[2] != JONGSUNG_LIST[0]:
            jungsung_count[JUNGSUNG_LIST.index(char_elements[1])] += 1

    print("Jungsung number:")
    for i in range(0, 21):
        print(JUNGSUNG_LIST[i], jungsung_count[i])

    print("Jongsung number:")

    for i in range(0, 28):
        print(JONGSUNG_LIST[i], jongsung_count[i])

    return case, jungsung_count, jongsung_count


def sort_elements(jungsung_count, jongsung_count):
    sorted_sound_list = list()
    sorted_jungsung_list = copy.deepcopy(JUNGSUNG_LIST)
    sorted_jongsung_list = copy.deepcopy(JONGSUNG_LIST)

    for i in range(1, 21):
        for j in range(0, 20):
            if jungsung_count[i] < jungsung_count[j]:
                temp = jungsung_count[i]
                jungsung_count[i] = jungsung_count[j]
                jungsung_count[j] = temp

                temp = sorted_jungsung_list[i]
                sorted_jungsung_list[i] = sorted_jungsung_list[j]
                sorted_jungsung_list[j] = temp

    for i in range(1, 28):
        for j in range(0, 27):
            if jongsung_count[i] < jongsung_count[j]:
                temp = jongsung_count[i]
                jongsung_count[i] = jongsung_count[j]
                jongsung_count[j] = temp

                temp = sorted_jongsung_list[i]
                sorted_jongsung_list[i] = sorted_jongsung_list[j]
                sorted_jongsung_list[j] = temp

    jung_index = 0
    jong_index = 0

    while jung_index < 21 and jong_index < 28:
        if jungsung_count[jung_index] <= jongsung_count[jong_index]:
            sorted_sound_list.append(sorted_jungsung_list[jung_index])
            jung_index += 1
        elif jungsung_count[jung_index] > jongsung_count[jong_index]:
            sorted_sound_list.append(sorted_jongsung_list[jong_index])
            jong_index += 1

    if jung_index < 21:
        for i in range(jung_index, 21):
            sorted_sound_list.append(sorted_jungsung_list[i])
    elif jong_index < 28:
        for i in range(jong_index, 28):
            sorted_sound_list.append(sorted_jongsung_list[i])

    return sorted_sound_list, sorted_jungsung_list, sorted_jongsung_list


def get_characters_with_element(element, labels):
    characters = list()
    for character in labels:
        character_elements = detach_character(character)
        if character_elements[1] == element or character_elements[2] == element:
            characters.append(character)

    return characters


def extract_basis_character(label_file):

    checked_chosung = list()
    for i in range(0, 6):
        checked_chosung.append(list())
        for j in range(0, 18):
            checked_chosung[i].append(0)

    checked_jungsung = list()
    for i in range(0, 6):
        checked_jungsung.append(list())
        for j in range(0, len(JUNGSUNG_CASE[i % 3])):
            checked_jungsung[i].append(0)

    checked_jongsung = list()
    basis_character_list = list()
    is_jongsung = False

    labels = read_character_file(label_file)

    case_list, jungsung_count, jongsung_count = classify_case(labels)

    sorted_sound_list, sorted_jungsung_list, sorted_jongsung_list = sort_elements(jungsung_count, jongsung_count)

    print(sorted_jungsung_list)
    print(jungsung_count)
    print(sorted_jongsung_list)
    print(jongsung_count)
    print(sorted_sound_list)

    # case 1~3
    for case_index in range(0, 3):
        chosung_count = list()
        sorted_chosung_list = copy.deepcopy(CHOSUNG_LIST)
        for i in range(0, len(CHOSUNG_LIST)):
            chosung_count.append(len(case_list[case_index][i]))

        for i in range(1, 19):
            for j in range(0, 18):
                if chosung_count[i] <= chosung_count[j]:
                    temp = chosung_count[i]
                    chosung_count[i] = chosung_count[j]
                    chosung_count[j] = temp

                    temp = sorted_chosung_list[i]
                    sorted_chosung_list[i] = sorted_chosung_list[j]
                    sorted_chosung_list[j] = temp

        for element in sorted_chosung_list:
            character_list = case_list[case_index][CHOSUNG_LIST.index(element)]
            for character in character_list:
                character_element = detach_character(character)

                if checked_jungsung[case_index][JUNGSUNG_CASE[case_index].index(character_element[1])] == min(checked_jungsung[case_index]):
                    basis_character_list.append(character)
                    checked_jungsung[case_index][JUNGSUNG_CASE[case_index].index(character_element[1])] += 1
                    break


        print(sorted_chosung_list)
        print(chosung_count)



    # case 4~6
    for element in sorted_sound_list:
        character_list = get_characters_with_element(element, labels)

        if element in JUNGSUNG_LIST:
            is_jongsung = False
        else:
            is_jongsung = True

        # if is_jongsung:
        #     #
        # else:
        #     #

        # print(character_list)


    return basis_character_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--label-file', type=str, dest='label_file',
                        default=DEFAULT_LABEL_FILE,
                        help='File containing newline delimited labels.')
    parser.add_argument('--output-dir', type=str, dest='output_dir',
                        default=DEFAULT_OUTPUT_DIR,
                        help='Output directory to store label CSV file.')
    args = parser.parse_args()
    basis_character_list = extract_basis_character(args.label_file)
    print(basis_character_list)

