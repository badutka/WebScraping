import time
import sys
from collections import defaultdict


def read_phrases(filename):
    lines = [line.rstrip('\n') for line in open(filename, encoding='utf-8')]
    return lines


def create_points_map():
    points_map = defaultdict(int)
    for letter in "aeinorswz":
        points_map.update({letter: 1})
    for letter in "cdklmpty":
        points_map.update({letter: 2})
    for letter in "bghjłu":
        points_map.update({letter: 3})
    for letter in "ąęfóśż":
        points_map.update({letter: 5})
    points_map.update({'ć': 6})
    points_map.update({'ń': 7})
    points_map.update({'ź': 9})

    return points_map


def search_phrases(phrases, char_dict, points_map):
    points_dict = {}
    points = 0

    for phrase in phrases:
        for char, amount in char_dict.items():
            number = phrase.count(char)
            if number <= amount:
                points += number * points_map[char]
            else:
                points += amount * points_map[char]
        points_dict[phrase] = points
        points = 0

    return points_dict


def default_char_dict(char_seq):
    char_dict = {char: char_seq.count(char) for char in char_seq}
    return char_dict


def count_max_points_for_phrase(phrase, points_map):
    points = 0
    for char in phrase:
        if char in points_map:
            points += points_map[char]
    return points


def count_max_points_for_chars(chars, points_map):
    points = 0
    for char in chars:
        if char in points_map:
            points += points_map[char]
    return points


def get_best_answer(points_dict: dict, points_map: dict, char_seq: str) -> 'prints answer':
    best = 0
    for v in points_dict.values():
        if v > best:
            best = v
    if best != 0:
        for k, v in points_dict.items():
            if v == best:
                print("Fraza: ", k, '\nPunkty: ', points_dict[k], '/', count_max_points_for_chars(char_seq, points_map))


def main():
    phrases = read_phrases('data.txt')
    points_map = create_points_map()
    # while True:
    # char_seq = input('Podaj litery, jedna po drugiej, bez spacji i innych znaków\n> ')
    # print(('Podaj litery, jedna po drugiej, bez spacji i innych znaków\n> '))
    char_seq = sys.argv[1]

    t0 = time.perf_counter()

    char_dict = default_char_dict(char_seq)
    points_dict = search_phrases(phrases, char_dict, points_map)
    get_best_answer(points_dict, points_map, char_seq)

    t1 = time.perf_counter()
    print("Czas: %.5f" % ((t1 - t0) * 1000.0), "ms\n")


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise Exception
    except Exception:
        print('Incorrect number of parameter!\nCorrect invocation should be: "python scrabble.py <string_of_characters>')
    main()
