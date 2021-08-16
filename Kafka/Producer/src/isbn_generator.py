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

        # Use the word if it is not empty otherwise recurse
        if word != "" and word is not None:
            isbn = isbnlib.isbn_from_words(word)
            
            # Return the isbn if it isn't empty otherwise recurse to get a valid isbn
            if isbn != "" and isbn is not None:
                return isbn
            else:
                return self.random_isbn()
        
        else:
            return self.random_isbn()