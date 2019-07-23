class Lemmatizer:
    lemmas_dict = {}

    def __init__(self):
        self.initialize_lemmas_dict()

    def initialize_lemmas_dict(self):
        with open('lemmas.txt', 'r', encoding="utf8") as lemmas:
            for row in lemmas:
                data = row.split('|')
                self.lemmas_dict.update({data[0]: data[1]})

    def lemmatize(self, array):
        lemmatized_array = []
        for word in array:
            lemmatized_array.append(self.__lemmatize_word(word))
        return lemmatized_array

    def __lemmatize_word(self, word):
        return self.lemmas_dict[word] if word in self.lemmas_dict else word
