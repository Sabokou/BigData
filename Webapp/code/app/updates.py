class Updates:

    def __init__(self):
        pass

    @staticmethod
    def format_sql_string(sql_str) -> str:
        sql_str = sql_str.replace("'None'", "NULL").replace("None", "NULL")
        return sql_str

    @staticmethod
    def update_book(list_book_obj, book_id=None) -> str:
        s_update = f''' UPDATE books
                        SET (n_book_edition, s_genre, n_publishing_year,
                            s_book_language, n_recommended_age, n_location_id, s_isbn) =
                            ({list_book_obj[0]}, '{list_book_obj[2]}', {list_book_obj[3]},
                             '{list_book_obj[1]}', {list_book_obj[5]}, {list_book_obj[4]}, {list_book_obj[6]})
                        WHERE n_book_id = (
                            SELECT n_book_id
                            FROM books
                            WHERE s_book_title = {list_book_obj[7]} AND n_book_edition = {list_book_obj[0]})
                        OR n_book_id = {book_id};'''

        s_update = s_update.replace("'None'", "NULL").replace("None", "NULL")
        return s_update

    @staticmethod
    def delete_book(book_id):
        s_delete = f"""DELETE FROM books WHERE n_book_id = {book_id};"""
        return s_delete


