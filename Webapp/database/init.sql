-- CREATE; INSERT; PROCEDURE; TRANSACTION; VIEW; 
-- Missing: SELECT; INSERT; 

-- Drop all old
DROP TABLE IF EXISTS LOAN;
DROP TABLE IF EXISTS BOOKS;


-- Create tables
CREATE TABLE BOOKS
(
    n_book_id         SERIAL UNIQUE NOT NULL,
    s_isbn            VARCHAR(13) UNIQUE,
    s_title           VARCHAR(4096) NOT NULL,
    n_publishing_year INT,
    s_book_language   CHAR(3),
    s_aut_first_name  VARCHAR(128),
    s_aut_last_name   VARCHAR(128),
    PRIMARY KEY (n_book_id)
);


CREATE TABLE LOAN
(
    n_loan_id         SERIAL UNIQUE NOT NULL,
    ts_now            TIMESTAMP     NOT NULL DEFAULT current_timestamp,
    n_book_id         INT           NOT NULL,
    PRIMARY KEY (n_loan_id),
    FOREIGN KEY (n_book_id) REFERENCES BOOKS (n_book_id) ON DELETE CASCADE
);

-- Insert Values into table

INSERT INTO BOOKS(s_isbn, s_title, n_publishing_year, s_book_language,
                   s_aut_first_name, s_aut_last_name)
VALUES ('9780575097568', 'Rivers of London', 2010, 'en', 'Ben', 'Aaronovitch'), 
       ('9780345524591', 'Moon Over Soho', 2011, NULL, 'Ben', 'Aaronovitch'),   
       ('9780525516019', 'A Land of Permanent Goodbyes',  NULL, 'en', 'Atia', 'Abawi'),  
       (NULL, 'Der Text des Lebens', NULL, 'de', 'Susanne', 'Abel'); 

INSERT INTO LOAN (ts_now, n_book_id)
VALUES ('2020-11-28 12:12:12', 1),
       ('2020-12-28 14:23:51', 2),
       ('2021-01-28 08:56:22', 3);


-- Create procedures
create or replace procedure add_book(
    author_first_name VARCHAR(128)[],
    author_last_name VARCHAR(128)[],
    publishing_year INT,
    book_title VARCHAR(4096),
    book_language CHAR(3),
    book_isbn VARCHAR(13)
)
    language plpgsql
AS
$$
DECLARE
    book_id      INT;

BEGIN

    INSERT INTO BOOKS(s_isbn, s_title, n_publishing_year, s_book_language, s_aut_first_name, s_aut_last_name)
        VALUES (book_isbn,
                book_title,
                publishing_year,
                book_language,
                author_first_name[1],
                author_last_name[1])
        RETURNING n_book_id INTO book_id;

END;
$$
;

create or replace procedure new_loan(
    book_id INT
)
    language plpgsql
AS
$$
DECLARE
    loan_id INT;
BEGIN

    INSERT INTO LOAN (ts_now, n_book_id)
    VALUES (now(), book_id)
    RETURNING n_loan_id INTO loan_id;

END;
$$; 