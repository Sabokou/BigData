-- CREATE; INSERT; PROCEDURE; TRANSACTION; VIEW; 
-- Missing: SELECT; INSERT; 

-- Drop all old
DROP VIEW IF EXISTS overview;
DROP VIEW IF EXISTS book_extended;
DROP TRIGGER IF EXISTS book_returned ON BORROW_ITEM;
DROP TABLE IF EXISTS WROTE;
DROP TABLE IF EXISTS READ_BOOKS;
DROP TABLE IF EXISTS BORROW_ITEM;
DROP TABLE IF EXISTS LOAN;
DROP TABLE IF EXISTS BOOKS;
DROP TABLE IF EXISTS PUBLISHER;
DROP TABLE IF EXISTS AUTHOR;



-- Create tables
CREATE TABLE AUTHOR
(
    n_author_id  SERIAL UNIQUE NOT NULL,
    s_first_name VARCHAR(128),
    s_last_name  VARCHAR(128)  NOT NULL,
    PRIMARY KEY (n_author_id)
);

CREATE TABLE PUBLISHER
(
    n_publisher_id SERIAL UNIQUE NOT NULL,
    s_pub_name     VARCHAR(128)  NOT NULL,
    PRIMARY KEY (n_publisher_id)
);


CREATE TABLE BOOKS
(
    n_book_id         SERIAL UNIQUE NOT NULL,
    s_isbn            VARCHAR(13) UNIQUE,
    s_title           VARCHAR(4096) NOT NULL,
    n_book_edition    INT           NOT NULL DEFAULT 1,
    s_genre           CHAR(20),
    n_publishing_year INT,
    s_book_language   CHAR(3),
    n_recommended_age INT,
    n_publisher_id    INT,
    PRIMARY KEY (n_book_id),
    FOREIGN KEY (n_publisher_id) REFERENCES PUBLISHER (n_publisher_id) ON DELETE SET NULL
);


CREATE TABLE LOAN
(
    n_loan_id SERIAL UNIQUE NOT NULL,
    ts_now    TIMESTAMP     NOT NULL DEFAULT current_timestamp,
    PRIMARY KEY (n_loan_id)
);


CREATE TABLE BORROW_ITEM
(
    n_borrow_item_id SERIAL UNIQUE NOT NULL,
    n_book_id        INT           NOT NULL,
    n_loan_id        INT           NOT NULL,
    b_active         BOOL          NOT NULL DEFAULT true,
    PRIMARY KEY (n_borrow_item_id),
    FOREIGN KEY (n_book_id) REFERENCES BOOKS (n_book_id) ON DELETE CASCADE,
    FOREIGN KEY (n_loan_id) REFERENCES LOAN (n_loan_id) ON DELETE CASCADE
);



CREATE TABLE WROTE
(
    n_wrote_id  SERIAL UNIQUE NOT NULL,
    n_book_id   INT           NOT NULL,
    n_author_id INT           NOT NULL,
    PRIMARY KEY (n_wrote_id),
    FOREIGN KEY (n_book_id) REFERENCES BOOKS (n_book_id) ON DELETE CASCADE,
    FOREIGN KEY (n_author_id) REFERENCES AUTHOR (n_author_id) ON DELETE CASCADE
);

-- Insert Values into table
INSERT INTO AUTHOR(s_first_name, s_last_name)
VALUES ('Ben', 'Aaronovitch'),
       ('Atia', 'Abawi'),
       ('Susanne', 'Abel');

INSERT INTO PUBLISHER(s_pub_name)
VALUES ('Heyne Verlag'),
       ('Akademische Arbeitsgemeinschaft Verlag'),
       ('Andiamo Verlag');

INSERT INTO BOOKS(s_isbn, s_title, n_book_edition, s_genre, n_publishing_year, s_book_language, n_recommended_age,
                   n_publisher_id)
VALUES ('9780575097568', 'Rivers of London', 1, 'Urban Fantasy', 2010, 'en', NULL, 1), -- Author 1
       ('9780345524591', 'Moon Over Soho', 2, 'Urban Fantasy', 2011, NULL, NULL, 1),   -- Author 1
       ('9780525516019', 'A Land of Permanent Goodbyes', 1, NULL, NULL, 'en', 18, 1),  -- Author 3
       (NULL, 'Der Text des Lebens', 1, NULL, NULL, 'de', 40, 2); -- Author 2

INSERT INTO LOAN (ts_now)
VALUES ('2020-11-28 12:12:12'),
       ('2020-12-28 14:23:51'),
       ('2021-01-28 08:56:22');

INSERT INTO BORROW_ITEM (n_book_id, n_loan_id)
VALUES (1, 2),
       (3, 2),
       (2, 1),
       (4, 3);

INSERT INTO WROTE(n_book_id, n_author_id)
VALUES (1, 1),
       (2, 1),
       (2, 3),
       (3, 3),
       (4, 2);



-- Create views
CREATE VIEW overview AS
SELECT books.n_book_id               BookID,
       books.s_title                 Title,
       books.n_publishing_year,
       books.s_isbn                  Isbn,
       STRING_AGG(s_last_name, ', ') Author,
       s_pub_name                    Publisher
FROM books
         LEFT JOIN wrote ON (books.n_book_id = wrote.n_book_id)
         LEFT JOIN author ON (wrote.n_author_id = author.n_author_id)
         LEFT JOIN publisher ON (books.n_publisher_id = publisher.n_publisher_id)
GROUP BY books.n_book_id, s_pub_name;

CREATE VIEW book_extended AS
SELECT books.n_book_id,
       books.s_isbn,
       books.s_title,
       books.n_book_edition,
       books.s_genre,
       books.n_publishing_year,
       books.s_book_language,
       books.n_recommended_age,
       author.s_first_name,
       author.s_last_name,
       publisher.s_pub_name
FROM books
         LEFT JOIN wrote ON (books.n_book_id = wrote.n_book_id)
         LEFT JOIN author ON (wrote.n_author_id = author.n_author_id)
         LEFT JOIN publisher ON (books.n_publisher_id = publisher.n_publisher_id)
GROUP BY books.n_book_id, wrote.n_wrote_id, author.n_author_id, publisher.n_publisher_id;



-- Create procedures
create or replace procedure add_book(
    author_first_name VARCHAR(128)[],
    author_last_name VARCHAR(128)[],
    publishing_year INT,
    publisher_name VARCHAR(128),
    book_title VARCHAR(4096),
    book_edition INT,
    book_language CHAR(3),
    book_genre CHAR(20),
    book_isbn VARCHAR(13),
    location_id INT DEFAULT NULL,
    recommended_age INT DEFAULT NULL
)
-- without addresses
    language plpgsql
AS
$$
DECLARE
    book_id      INT;
    loop_counter INT;

BEGIN


    FOR loop_counter IN 1..(cardinality(author_last_name))
        LOOP
            IF NOT EXISTS(SELECT n_author_id
                          FROM author
                          WHERE author_last_name[loop_counter] = s_last_name
                            AND author_first_name[loop_counter] = s_first_name
                )
            THEN
                INSERT INTO AUTHOR(s_first_name, s_last_name)
                VALUES (author_first_name[loop_counter], author_last_name[loop_counter]);
            END IF;
        END LOOP;


    IF publisher_name IS NOT NULL THEN
        IF NOT EXISTS(SELECT n_publisher_id
                      FROM PUBLISHER
                      WHERE publisher_name = s_pub_name
            )
        THEN
            INSERT INTO PUBLISHER(s_pub_name)
            VALUES (publisher_name);
        END IF;
    END IF;

    IF NOT EXISTS(SELECT n_book_id
                  FROM books
                  WHERE book_isbn = s_isbn
                     OR (book_title = s_title AND book_edition = n_book_edition AND book_language = s_book_language)
        )
    THEN
        INSERT INTO BOOKS(s_isbn, s_title, n_book_edition, s_genre, n_publishing_year, s_book_language,
                          n_recommended_age, n_publisher_id)
        VALUES (book_isbn,
                book_title,
                book_edition,
                book_genre,
                publishing_year,
                book_language,
                recommended_age,
                (SELECT n_publisher_id FROM PUBLISHER WHERE publisher_name = s_pub_name))
        RETURNING n_book_id INTO book_id;
        FOR loop_counter IN 1..(cardinality(author_first_name))
            LOOP
                INSERT INTO WROTE(n_book_id, n_author_id)
                VALUES (book_id,
                        (SELECT n_author_id
                         FROM author
                         WHERE author_last_name[loop_counter] = s_last_name
                           AND author_first_name[loop_counter] = s_first_name));
            END LOOP;
    END IF;


END;
$$
;
