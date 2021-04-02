-- CREATE; PROCEDURE; TRIGGER; TRANSACTION; VIEW; 
-- Missing: SELECT; INSERT; 

-- Drop all old
DROP VIEW IF EXISTS overview;
DROP VIEW IF EXISTS book_extended;
DROP TRIGGER IF EXISTS book_returned ON BORROW_ITEM;
DROP TABLE IF EXISTS WROTE;
DROP TABLE IF EXISTS READ_BOOKS;
DROP TABLE IF EXISTS BORROW_ITEM;
DROP TABLE IF EXISTS LOAN;
DROP TABLE IF EXISTS USERS;
DROP TABLE IF EXISTS BOOKS;
DROP TABLE IF EXISTS PUBLISHER;
DROP TABLE IF EXISTS AUTHOR;



-- Create tables


CREATE TABLE AUTHOR
(
    n_author_id  SERIAL UNIQUE NOT NULL,
    s_first_name VARCHAR(128),
    s_last_name  VARCHAR(128)  NOT NULL,
    PRIMARY KEY (n_author_id),
);

CREATE TABLE PUBLISHER
(
    n_publisher_id SERIAL UNIQUE NOT NULL,
    s_pub_name     VARCHAR(128)  NOT NULL,
    PRIMARY KEY (n_publisher_id),
);




CREATE TABLE BOOKS
(
    n_book_id         SERIAL UNIQUE NOT NULL,
    s_isbn            VARCHAR(13) UNIQUE,
    s_title           VARCHAR(4096) NOT NULL,
    n_book_edition    INT NOT NULL DEFAULT 1,
    s_genre           CHAR(20),
    n_publishing_year INT,
    s_book_language   CHAR(3),
    n_recommended_age INT,
    b_is_available    BOOL          NOT NULL,
    n_publisher_id    INT,
    PRIMARY KEY (n_book_id),
    FOREIGN KEY (n_publisher_id) REFERENCES PUBLISHER (n_publisher_id),
);

CREATE TABLE USERS
(
    n_user_id        SERIAL UNIQUE NOT NULL,
    s_user_name      VARCHAR(128) UNIQUE NOT NULL,
    s_password       VARCHAR(128)  NOT NULL,
    s_first_name     VARCHAR(128),
    s_last_name      VARCHAR(128),

    dt_date_of_birth DATE,
    PRIMARY KEY (n_user_id),
);

CREATE TABLE LOAN
(
    n_loan_id SERIAL UNIQUE NOT NULL,
    ts_now    TIMESTAMP     NOT NULL DEFAULT current_timestamp,
    n_user_id INT           NOT NULL,
    PRIMARY KEY (n_loan_id),
    FOREIGN KEY (n_user_id) REFERENCES USERS (n_user_id)
);


CREATE TABLE BORROW_ITEM
(
    n_borrow_item_id SERIAL UNIQUE NOT NULL,
    n_duration       INT           NOT NULL, --in days
    n_book_id        INT           NOT NULL,
    n_loan_id        INT           NOT NULL,
    b_active         BOOL          NOT NULL DEFAULT true,
    PRIMARY KEY (n_borrow_item_id),
    FOREIGN KEY (n_book_id) REFERENCES BOOKS (n_book_id),
    FOREIGN KEY (n_loan_id) REFERENCES LOAN (n_loan_id)
);


CREATE TABLE READ_BOOKS
(
    n_read_books_id SERIAL UNIQUE NOT NULL,
    n_book_id       INT           NOT NULL,
    n_user_id       INT           NOT NULL,
    PRIMARY KEY (n_read_books_id),
    FOREIGN KEY (n_book_id) REFERENCES BOOKS (n_book_id),
    FOREIGN KEY (n_user_id) REFERENCES USERS (n_user_id)
);



CREATE TABLE WROTE
(
    n_wrote_id  SERIAL UNIQUE NOT NULL,
    n_book_id   INT           NOT NULL,
    n_author_id INT           NOT NULL,
    PRIMARY KEY (n_wrote_id),
    FOREIGN KEY (n_book_id) REFERENCES BOOKS (n_book_id),
    FOREIGN KEY (n_author_id) REFERENCES AUTHOR (n_author_id)
);

-- Inserts into tables

INSERT INTO AUTHOR(s_first_name, s_last_name)
VALUES ('Ben', 'Aaronovitch'),
       ('Atia', 'Abawi'),
       ('Susanne', 'Abel');

INSERT INTO PUBLISHER(s_pub_name)
VALUES ('Heyne Verlag'),
       ('Akademische Arbeitsgemeinschaft Verlag'),
       ('Andiamo Verlag');


INSERT INTO BOOKS(s_isbn, s_title, n_book_edition, s_genre, n_publishing_year, s_book_language, n_recommended_age,
                  b_is_available, n_publisher_id)
VALUES ('9780575097568', 'Rivers of London', 1, 'Urban Fantasy', 2010, 'en', NULL, true, 1),   -- Author 1
       ('9780345524591', 'Moon Over Soho', 2, 'Urban Fantasy', 2011, NULL, NULL, true, 1),     -- Author 1
       ('9780525516019', 'A Land of Permanent Goodbyes', 1, NULL, NULL, 'en', 18, true, 1), -- Author 3
       (NULL, 'Der Text des Lebens', 1, NULL, NULL, 'de', 40, true, 2); -- Author 2

INSERT INTO USERS(s_user_name, s_password,s_first_name, s_last_name, dt_date_of_birth)
VALUES ('benni', '1234', 'Ben', 'Hell', DATE '1987-04-03'),
       ('nadia', '1234', 'Nadia', 'Tall', DATE '1968-10-31',
       ('susi', '1234', 'Susanne', 'Nieble', DATE'2001-02-25');

INSERT INTO LOAN (ts_now, n_user_id)
VALUES ('2020-11-28 12:12:12', 1),
       ('2020-12-28 14:23:51', 2),
       ('2021-01-28 08:56:22', 3);

INSERT INTO BORROW_ITEM (n_duration, n_book_id, n_loan_id, b_active)
VALUES (14, 1, 2, false),
       (7, 3, 2, false),
       (7, 2, 1, false),
       (21, 4, 3, false);

INSERT INTO READ_BOOKS(n_book_id, n_user_id)
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


    IF NOT EXISTS(SELECT n_publisher_id
                  FROM PUBLISHER
                  WHERE publisher_name = s_pub_name
        )
    THEN
        INSERT INTO PUBLISHER(s_pub_name)
        VALUES (publisher_name);
    END IF;

    IF NOT EXISTS(SELECT n_book_id
                  FROM books
                  WHERE book_isbn = s_isbn
                     OR (book_title = s_title AND book_edition = n_book_edition AND book_language = s_book_language)
        )
    THEN
        INSERT INTO BOOKS(s_isbn, s_title, n_book_edition, s_genre, n_publishing_year, s_book_language,
                          n_recommended_age, b_is_available, n_publisher_id)
        VALUES (book_isbn,
                book_title,
                book_edition,
                book_genre,
                publishing_year,
                book_language,
                recommended_age,
                true,
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

CREATE OR REPLACE FUNCTION book_returned_triggered()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
AS
$$
BEGIN
    IF new.b_active <> old.b_active then
        UPDATE books
        SET b_is_available = true
        WHERE books.n_book_id = new.n_book_id;
    END if;

    RETURN NEW;
END;
$$;


-- Create trigger
CREATE TRIGGER book_returned
    AFTER UPDATE
    ON borrow_item
    FOR EACH ROW
EXECUTE PROCEDURE book_returned_triggered();

create or replace procedure new_loan(
    loan_user int,
    book_ids INT[],
    duration int
)
    language plpgsql
AS
$$
DECLARE
    book    INT;
    loan_id INT;
BEGIN

    INSERT INTO LOAN (ts_now, n_user_id)
    VALUES (now(), loan_user)
    RETURNING n_loan_id INTO loan_id;


    FOREACH book IN ARRAY $2
        LOOP
            INSERT INTO BORROW_ITEM (n_duration, n_book_id, n_loan_id)
            VALUES (duration, book, loan_id);

            UPDATE books
            SET b_is_available = false
            WHERE n_book_id = book;
        END loop;


END;
$$;