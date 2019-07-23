import os
import re
from math import *
from indekser.Lemmatizer import *

words_re = re.compile(r'\w+', re.UNICODE)
words_re2 = re.compile(r'^\D*$')
N = 0
lemmatizer = Lemmatizer()
do_lemmatize: bool = 1


def count_unique_words(unique_words_list: list, unique_words_dict: dict) -> dict:
    for word in unique_words_list:
        if word in unique_words_dict:
            unique_words_dict[word] += 1
        else:
            unique_words_dict[word] = 1

    return unique_words_dict


def create_words_list(file: str) -> list:
    text = file.read()
    text = text.replace('_', '')
    words_list = [word.lower() for word in words_re.findall(text) if
                  word != '-' and words_re2.match(word) is not None]

    return words_list


def read_all_files_and_crate_unique_words_dict(path: str) -> dict: # sub-folder path!
    unique_words_dict = {}
    global N

    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            N += 1
            with open(os.path.join(dirname, filename), 'r', encoding="utf8") as file: # encoding utf-8?
                words_list = create_words_list(file)
                unique_words_list = list(set(words_list))

                if do_lemmatize == 0:
                    pass  # unique_words_list is already okay, possible deletion of this if statement

                if do_lemmatize == 1:
                    unique_words_list = lemmatizer.lemmatize(unique_words_list)

                unique_words_dict = count_unique_words(unique_words_list, unique_words_dict)

    return unique_words_dict


def calculate_idfi(path: str) -> dict:
    unique_words_dict = read_all_files_and_crate_unique_words_dict(path)

    for key in unique_words_dict:
        unique_words_dict[key] = log(N/unique_words_dict[key], 10)

    return unique_words_dict


def create_occurences_dicts(words_list, number_of_occurences_dict, word_occurences):
    for word in words_list:

        if word in number_of_occurences_dict:
            number_of_occurences_dict[word] += 1
        else:
            number_of_occurences_dict[word] = 1

        if word in word_occurences:
            word_occurences[word] += 1
        else:
            word_occurences[word] = 1

    return number_of_occurences_dict, word_occurences


def calculate_weights_and_create_indexer(path: str) -> 'saves weights':
    word_occurences = {}
    idfi = calculate_idfi(path)

    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            with open(os.path.join(dirname, filename), 'r', encoding="utf8") as file: # encoding utf-8?
                words_list = create_words_list(file)
                unique_words_list = list(set(words_list))
                number_of_occurences_dict = {}

                if do_lemmatize == 0:
                    number_of_occurences_dict, word_occurences = create_occurences_dicts(words_list,
                                                                                         number_of_occurences_dict,
                                                                                         word_occurences)
                if do_lemmatize == 1:
                    unique_words_list = lemmatizer.lemmatize(unique_words_list)
                    words_list = lemmatizer.lemmatize(words_list)
                    number_of_occurences_dict, word_occurences = create_occurences_dicts(words_list,
                                                                                         number_of_occurences_dict,
                                                                                         word_occurences)

                term_frequency_dict = {k: number_of_occurences_dict[k]/len(words_list) for k in unique_words_list}
                term_weights = {k: term_frequency_dict[k]*idfi[k] for k in unique_words_list}
                save_data(os.path.join(dirname, filename), term_weights)
    # print(word_occurences)
    return 0


def save_data(path: str, term_weights: dict) -> 'saves data': #nazwa folderu i pliku, lista termow wraz z waga
    if do_lemmatize == 1:
        print('lemmatized', path, term_weights)
    else:
        print(path, term_weights)


def f1(l1: list, tf: bool) -> '': #lista termow w kolejnosci malejacej
    pass
