import matplotlib
from collections import Counter
import matplotlib.pyplot as plt
import time


def read_words_from_file():
    # f = open("words.txt", "r", encoding='utf-8')
    # contents = f.read()
    # print(contents)
    with open('words.txt', 'r', encoding="utf-8") as file:
        lines = file.readlines()
        words_list = [line[:-1] for line in lines]
    return words_list


def plot_stats(words_list):

    # ===== WYKRES KOLOWY =====

    data = Counter(words_list).most_common(30)
    length = len(words_list)
    print(data)
    print(len(words_list))
    print(type(data[0]))

    sizes, labels = [i[1] for i in data], [i[0] for i in data]
    plt.pie(sizes, labels=labels, autopct='%1.2f%%')
    plt.show()

    counter = 0
    for i in range(1, len(words_list)):
        if words_list[i] not in words_list[:i]:
            counter += 1
        if i == 10000:
            print(counter)

    # ===== WYKRES CZESTOSCI =====

    arguments = []
    values = []
    num = len(words_list)
    k = 500000

    for i in range(1, num, k):
        arguments.append(i)
        values.append(len(set(words_list[:i])))


    plt.plot(arguments, values, 'ro')
    plt.axis([0, 1.05*num, 0, 1.05*num])
    plt.xlabel('Ilosc slow')
    plt.ylabel('Ilosc unikalnych slow')
    plt.show()

    # ===== WYKRES POKRYCIA =====

    data = Counter(words_list).most_common(1000)
    length = len(words_list)

    val = [i[1] for i in data]
    vals = [i/length for i in val]
    # vals2 = []
    # for i in range(0, 1000):
    #     vals2.append(sum(val[0:i+i]))
    # print(vals2)
    # vals3 = [i/length for i in vals2]
    # print(vals)
    args = [i for i in range(0, 1000)]

    plt.plot(args, vals)
    plt.xlabel('slowa')
    plt.ylabel('pokrycie tekstu')
    # plt.show()


def main():
    words_list = read_words_from_file()
    plot_stats(words_list)


if __name__ == "__main__":
    main()



