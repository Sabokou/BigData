class Selections:

    def __init__(self):
        pass

    @staticmethod
    def sql_read_books(s_user):
        s_book_ids = f'SELECT n_book_id FROM read_books WHERE n_user_id = {s_user}'
        s_sql = f'SELECT title, author, publisher, isbn  FROM overview WHERE bookid IN ({s_book_ids});'
        return s_sql

    @staticmethod
    def sql_all_book_information(s_book_id=None):
        if s_book_id is None:
            s_sql = """
            SELECT 
                b.s_isbn AS ISBN,
                b.s_title AS Booktitle, 
                b.n_book_edition AS Bookedition, 
                b.s_genre AS Bookgenre,
                b.dt_publishing_date AS "Publishing date",
                b.s_book_language AS "Book language",
                b.n_recommended_age AS "Recommended Age",
                b.b_is_availalbe AS Availabilty, 
                au.s_first_name AS "Author's first name", 
                au.s_last_name AS "Author's last name",
                l.s_compartment AS "Location:compartment", 
                l.s_shelf AS "Location:shelf", 
                l.s_room AS "Location:room", 
                l.n_loc_floor AS "Location:floor", 
                ad.s_street AS "Location:street", 
                ad.s_house_number AS "Location: house_number", 
                ad.s_city AS "Location:city", 
                ad.s_country AS "Location:country", 
                ad.n_zipcode AS "Location:zipcode", 
                pu.s_pub_name AS Publisher
            FROM books AS b
                LEFT JOIN wrote AS w ON b.n_book_id =  w.n_book_id
                LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
                LEFT JOIN lib_location AS l ON b.n_location_id = l.n_location_id
                LEFT JOIN addresses AS ad ON l.n_address_id = ad.n_address_id
                LEFT JOIN publisher AS pu ON b.n_publisher_id = pu.n_publisher_id;
            """
        else:
            s_sql = f"""
            SELECT 
                b.s_isbn AS ISBN, 
                b.s_title AS Booktitle, 
                b.n_book_edition AS Edition, 
                b.s_genre AS Genre,
                b.dt_publishing_date AS "Publishing date", 
                b.s_book_language AS "Book language", 
                b.n_recommended_age AS "Recommended Age",
                b.b_is_availalbe AS Availabilty, 
                au.s_first_name AS "Author's first name", 
                au.s_last_name AS "Author's last name",
                l.s_compartment AS "Location:compartment", 
                l.s_shelf AS "Location:shelf", 
                l.s_room AS "Location:room", 
                l.n_loc_floor AS "Location:floor", 
                ad.s_street AS "Location:street", 
                ad.s_house_number AS "Location: house_number", 
                ad.s_city AS "Location:city", 
                ad.s_country AS "Location:country", 
                ad.n_zipcode AS "Location:zipcode", 
                pu.s_pub_name AS Publisher
            FROM books AS b
                LEFT JOIN wrote AS w ON b.n_book_id =  w.n_book_id
                LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
                LEFT JOIN lib_location AS l ON b.n_location_id = l.n_location_id
                LEFT JOIN addresses AS ad ON l.n_address_id = ad.n_address_id
                LEFT JOIN publisher AS pu ON b.n_publisher_id = pu.n_publisher_id
            WHERE b.n_book_id = {s_book_id};
            """
        return s_sql

    @staticmethod
    def sql_user_active_loans(s_user_id=None):
        if s_user_id is None:
            s_sql = """
            SELECT 
                bo.n_book_id as action, 
                u.s_first_name AS "User's first name", 
                u.s_last_name AS "User's last name", 
                l.n_loan_id AS "Loan id",
                l.ts_now AS "Loan timestamp", 
                bi.n_duration AS "Loan duration", 
                bi.b_active AS "Loan status", 
                bo.s_isbn AS "Book ISBN",
                bo.s_title AS "Book title", 
                bo.n_book_edition AS "Book edition"
            FROM users AS u 
                LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
                LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
                LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
            WHERE bi.b_active = 'true';
            """
        else:
            s_sql = f"""
            SELECT 
                u.s_first_name AS "User's first name", 
                u.s_last_name AS "User's last name", 
                l.n_loan_id AS "Loan id",
                l.ts_now AS "Loan timestamp", 
                bi.n_duration AS "Loan duration", 
                bi.b_active AS "Loan status", 
                bo.s_isbn AS "ISBN",
                bo.s_title AS "Book title", 
                bo.n_book_edition AS "Book edition"
            FROM users AS u
                LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
                LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
                LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
            WHERE bi.b_active = 'true' and u.n_user_id = {s_user_id};
            """
        return s_sql

    @staticmethod
    def sql_books_for_certain_genre_or_language(s_genre=None, s_language=None):
        if s_genre is None and s_language is None:
            s_sql = """
            SELECT 
                b.s_isbn AS ISBN, 
                b.s_title AS Booktitle, 
                b.n_book_edition AS Bookedition, 
                b.s_genre AS Book_genre, 
                b.s_book_language AS Book_language
            FROM books AS b;
            """
        elif s_genre is not None and s_language is None:
            s_sql = f"""
            SELECT 
                b.s_isbn AS ISBN,
                b.s_title AS Booktitle, 
                b.n_book_edition AS Bookedition, 
                b.s_genre AS Book_genre, 
                b.s_book_language AS Book_language
            FROM books AS b
            WHERE b.s_genre = {s_genre};
            """
        elif s_genre is None and s_language is not None:
            s_sql = f"""
            SELECT 
                b.s_isbn AS ISBN, 
                b.s_title AS Booktitle, 
                b.n_book_edition AS Bookedition, 
                b.s_genre AS Book_genre, 
                b.s_book_language AS Book_language
            FROM books AS b
            WHERE b.s_book_language = {s_language};
            """
        else:
            s_sql = f"""
            SELECT 
                b.s_isbn AS ISBN, 
                b.s_title AS Booktitle, 
                b.n_book_edition AS Bookedition, 
                b.s_genre AS Book_genre, 
                b.s_book_language AS Book_language
            FROM books AS b
            WHERE b.s_book_language = {s_language} and b.s_genre = {s_genre};
            """
        return s_sql


