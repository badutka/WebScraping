import os


def join_text_files(path):
    words = ""

    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            file = path + "/" + filename
            f = open(file, "r", encoding="utf-8")
            words += f.read()

    return words


def replace_chars(words):
    for c in "•”„–²:;—.,()-%·1234567890":
        words = words.replace(c, " ")
    words = words.lower().split()
    # print(len(words))

    return words


def save_to_single_file(words):
    with open('words.txt', mode='wt', encoding='utf-8') as myfile:
        for lines in words:
            print(lines, file=myfile)
    myfile.close()


def main():
    path = 'E:/Projects/PycharmProjects/MainProjects/PJN_lab/tutorial/zapisy'
    words = join_text_files(path)
    words = replace_chars(words)
    save_to_single_file(words)


if __name__ == "__main__":
    main()

