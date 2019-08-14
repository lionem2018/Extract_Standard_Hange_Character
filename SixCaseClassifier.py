import io
import os
import argparse
import csv


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
    # print('초성 : {}'.format(CHOSUNG_LIST[char1]))
    char2 = int((char_code - (CHOSUNG_SET_NUMBER * char1)) / JUNGSUNG_NUMBER)
    result.append(JUNGSUNG_LIST[char2])
    # print('중성 : {}'.format(JUNGSUNG_LIST[char2]))
    char3 = int((char_code - (CHOSUNG_SET_NUMBER * char1) - (JUNGSUNG_NUMBER * char2)))
    result.append(JONGSUNG_LIST[char3])

    return result


def count_case_number(case_list):

    pre_char1 = ' '
    count = 0

    for character in case_list:
        char_code = ord(character) - BASE_CODE
        char1 = int(char_code / CHOSUNG_SET_NUMBER)

        if pre_char1 != char1:
            count += 1
            pre_char1 = char1

    return count


def classify(labels, output_dir):

    labels_csv = io.open(os.path.join(output_dir, 'labels-map.csv'), 'w', encoding='utf-8')
    line_for_draw = "========================================"
    jongsung_count = list()
    jungsung_count = list()
    pre_char1 = ' '
    case = list()

    for i in range(0, 6):
        case.append([])

    for i in range(0, 19):
        for j in range(0, 6):
            if j < 3:
                case[j].append([" ", " ", " ", " ", " ", " ", " ", " ", " "])
            else:
                case[j].append([])

    for i in range(0, 28):
        jongsung_count.append(0)

    for i in range(0, 21):
        jungsung_count.append(0)

    for character in labels:
        char_elements = detach_character(character)
        # print("".join(char_elements))
        if char_elements[2] == JONGSUNG_LIST[0]:
            if char_elements[1] in JUNGSUNG_CASE[0]:
                # case[0][CHOSUNG_LIST.index(char_elements[0])].append(character)
                case[0][CHOSUNG_LIST.index(char_elements[0])].insert(JUNGSUNG_CASE[0].index(char_elements[1]), character)
            elif char_elements[1] in JUNGSUNG_CASE[1]:
                # case[1][CHOSUNG_LIST.index(char_elements[0])].append(character)
                case[1][CHOSUNG_LIST.index(char_elements[0])].insert(JUNGSUNG_CASE[1].index(char_elements[1]),
                                                                     character)
            else:
                # case[2][CHOSUNG_LIST.index(char_elements[0])].append(character)
                case[2][CHOSUNG_LIST.index(char_elements[0])].insert(JUNGSUNG_CASE[2].index(char_elements[1]),
                                                                     character)
        else:
            if char_elements[1] in JUNGSUNG_CASE[0]:
                case[3][CHOSUNG_LIST.index(char_elements[0])].append(character)
                # case[3][CHOSUNG_LIST.index(char_elements[0])].insert(JUNGSUNG_CASE[0].index(char_elements[1]),
                                                                     # character)
            elif char_elements[1] in JUNGSUNG_CASE[1]:
                case[4][CHOSUNG_LIST.index(char_elements[0])].append(character)
                # case[4][CHOSUNG_LIST.index(char_elements[0])].insert(JUNGSUNG_CASE[1].index(char_elements[1]),
                                                                     # character)
            else:
                case[5][CHOSUNG_LIST.index(char_elements[0])].append(character)
                # case[5][CHOSUNG_LIST.index(char_elements[0])].insert(JUNGSUNG_CASE[2].index(char_elements[1]),
                #                                                      character)

        jongsung_count[JONGSUNG_LIST.index(char_elements[2])] += 1

        if char_elements[2] != JONGSUNG_LIST[0]:
        #     if pre_char1 != char_elements[1]:
            jungsung_count[JUNGSUNG_LIST.index(char_elements[1])] += 1
                # pre_char1 = char_elements[1]

        ###
        # if char_elements[2] == JONGSUNG_LIST[10]:
        #     print(character)
        #
        # if char_elements[1] == JUNGSUNG_LIST[9] and char_elements[2] != JONGSUNG_LIST[0]:
        #     print(character)

        if char_elements[1] == 'ㅞ' and char_elements[2] == 'ㅂ':
            print(character)

        ###

    writer = csv.writer(labels_csv)

    for i in range(0, 6):
        writer.writerow(JUNGSUNG_CASE[(i % 3)])

        for j in range(0, 19):
            writer.writerow(case[i][j])

        writer.writerow(line_for_draw)
        # labels_csv.write(u'{},{}\n'.format(file_path, character))

    # print("case1:", count_case_number(case[0]))
    # print("case2:", count_case_number(case[1]))
    # print("case3:", count_case_number(case[2]))
    # print("case4:", count_case_number(case[3]))
    # print("case5:", count_case_number(case[4]))
    # print("case6:", count_case_number(case[5]))

    print("Jungsung number:")
    print(jungsung_count)
    print("Jongsung number:")
    print(jongsung_count)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--label-file', type=str, dest='label_file',
                        default=DEFAULT_LABEL_FILE,
                        help='File containing newline delimited labels.')
    parser.add_argument('--output-dir', type=str, dest='output_dir',
                        default=DEFAULT_OUTPUT_DIR,
                        help='Output directory to store label CSV file.')
    args = parser.parse_args()
    classify(read_character_file(args.label_file), args.output_dir)

