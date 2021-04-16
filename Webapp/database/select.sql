--  The first query selects all basic information to all books, as i.e. author, title, ISBN, Location, Publisher... . 

SELECT b.s_isbn             AS ISBN,
       b.s_title            AS Booktitle,
       b.n_book_edition     AS Bookedition,
       b.s_genre            AS Bookgenre,
       b.n_publishing_year  AS Publishingdate,
       b.s_book_language    AS Booklenguage,
       b.n_recommended_age  AS Recommended_Age,
       au.s_first_name      AS Author_first_name,
       au.s_last_name       AS Author_last_name,
       pu.s_pub_name        AS Publisher
FROM books AS b
         LEFT JOIN wrote AS w ON b.n_book_id = w.n_book_id
         LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
         LEFT JOIN publisher AS pu ON b.n_publisher_id = pu.n_publisher_id;


-- The queries select all books from a certain genre or language.

SELECT b.s_isbn          AS ISBN,
       b.s_title         AS Booktitle,
       b.n_book_edition  AS Bookedition,
       b.s_genre         AS Book_genre,
       b.s_book_language AS Book_language
FROM books AS b
WHERE b.s_genre = 'Urban Fantasy';

SELECT b.s_isbn          AS ISBN,
       b.s_title         AS Booktitle,
       b.n_book_edition  AS Bookedition,
       b.s_genre         AS Book_genre,
       b.s_book_language AS Book_language
FROM books AS b
WHERE b.s_book_language = 'en';

