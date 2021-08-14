# pip install isbnlib
# pip install Random-Word
import isbnlib
from random_word import RandomWords

class ISBN_generator():
    def __init__(self):
        self.word_gen = RandomWords()

    def random_word(self):
        # get a random word that is common; found in at leased 10 dictionaries
        return self.word_gen.get_random_word(hasDictionaryDef="true", minDictionaryCount=10)

    def random_isbn(self):
        word = self.random_word()
        isbn = isbnlib.isbn_from_words(word)
        success = (isbn != "")
        # Return the isbn if it isn't empty otherwise recurse to get a valid isbn
        if success:
            return isbn
        else:
            return self.isbn_from_random_word()