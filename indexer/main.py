from indekser.indexer import *


def main():
    # path = 'korpus'
    path = 'E:\Projects\PycharmProjects\MainProjects\PJN_lab\\tutorial\zapisy1'
    # print(read_all_files_and_crate_unique_words_dict.__annotations__)
    calculate_weights_and_create_indexer(path)


if __name__ == "__main__":
    main()
