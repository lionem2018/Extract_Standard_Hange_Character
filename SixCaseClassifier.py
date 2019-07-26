import io
import os
import argparse


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


def classfy(labels, output_dir):

    labels_csv = io.open(os.path.join(output_dir, 'labels-map.csv'), 'w', encoding='utf-8')

    for character in labels:
        char_elements = detach_character(character)
        print("".join(char_elements))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--label-file', type=str, dest='label_file',
                        default=DEFAULT_LABEL_FILE,
                        help='File containing newline delimited labels.')
    parser.add_argument('--output-dir', type=str, dest='output_dir',
                        default=DEFAULT_OUTPUT_DIR,
                        help='Output directory to store label CSV file.')
    args = parser.parse_args()
    classfy(read_character_file(args.label_file), args.output_dir)

