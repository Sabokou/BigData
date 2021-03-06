import logging

import isbnlib


class Book:

    def __init__(self) -> object:
        self.author_first_names = None
        self.author_last_names = None
        self.book_title = None
        self.book_language = None
        self.book_isbn = None
        self.publishing_year = None

    def set_via_isbn(self, s_isbn: str = "9780062893338"):
        # remove "-" from isbn string
        s_isbn = "".join(s_isbn.strip("-"))

        # check if google books has information on the isbn
        meta_google = isbnlib.meta(s_isbn, service='goob')
        if bool(meta_google) is False:  # empty dict => False | not empty => use found meta_data
            # fetch data from wiki api
            logging.info("Book not found in Google API")
            meta_wiki = isbnlib.meta(s_isbn, service='wiki')

            # check if wikipedia api has information on the isbn
            if bool(meta_wiki) is False:  # empty dict => False | not empty => use found meta_data
                # fetch data from openlibrary api
                logging.info("Book not found in Wiki API")
                meta_open = isbnlib.meta(s_isbn, service='openl')

                # check if openlibrary api has information on the isbn
                if bool(meta_open) is False:  # empty dict => False | not empty => use found meta_data
                    # if not => no information could be found on the isbn
                    logging.warning("Book not found in any APIs")
                    print("Book not found!")
                    return None
                else:
                    meta_data = meta_open
            else:
                meta_data = meta_wiki
        else:
            meta_data = meta_google

        self.author_first_names = []
        self.author_last_names = []
        for author in meta_data['Authors']:
            name = author.split(" ")
            last_name = name.pop(-1)
            first_names = " ".join(name)
            self.author_first_names.append(last_name)
            self.author_last_names.append(first_names)

        self.book_title = meta_data["Title"]
        self.book_language = meta_data["Language"]
        self.publishing_year = meta_data['Year']
        self.book_isbn = list(meta_data.values())[0]


    def get_s_sql_call(self) -> str or None:

        if self.book_title is None:
            return None
        # if self.publisher_name is None:
        #     return None
        if self.author_last_names is None:
            return None

        call = f"""CALL add_book(
                        ARRAY{self.author_first_names}, 
                        ARRAY{self.author_last_names},
                        {self.publishing_year}, 
                        '{self.book_title}', 
                        '{self.book_language}', 
                        '{self.book_isbn}');"""

        call = call.replace("'None'", "NULL").replace("None", "NULL")
        # print(call)
        return call