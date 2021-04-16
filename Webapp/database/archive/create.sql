DROP TABLE IF EXISTS WROTE;
DROP TABLE IF EXISTS READ_BOOKS;
DROP TABLE IF EXISTS BORROW_ITEM;
DROP TABLE IF EXISTS LOAN;
DROP TABLE IF EXISTS BOOKS;
DROP TABLE IF EXISTS PUBLISHER;
DROP TABLE IF EXISTS AUTHOR;




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
    PRIMARY KEY (n_loan_id),
);


CREATE TABLE BORROW_ITEM
(
    n_borrow_item_id SERIAL UNIQUE NOT NULL,
    n_duration       INT           NOT NULL, --in days
    n_book_id        INT           NOT NULL,
    n_loan_id        INT           NOT NULL,
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