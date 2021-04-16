INSERT INTO AUTHOR(s_first_name, s_last_name)
VALUES
('Aaronovitch', 'Ben'),
('Abawi', 'Atia'),
('Abel', 'Susanne');

INSERT INTO PUBLISHER(s_pub_name)
VALUES
('Heyne Verlag'),
('Akademische Arbeitsgemeinschaft Verlag'),
('Andiamo Verlag');


INSERT INTO BOOKS(s_isbn, s_title, n_book_edition, s_genre, dt_publishing_date, s_book_language, n_recommended_age, n_publisher_id)
VALUES
('9780575097568', 'Rivers of London', 1, 'Urban Fantasy', DATE '2011-01-10', 'en', NULL, 1), -- Author 1
('9780345524591', 'Moon Over Soho', 2, 'Urban Fantasy', DATE '2011-04-21', NULL , NULL, 1),  -- Author 1
('9780525516019', 'A Land of Permanent Goodbyes', NULL, NULL, NULL, 'en', 18,  1), -- Author 3
(NULL, 'Der Text des Lebens', NULL, NULL, NULL, 'de', 40,  2); -- Author 2 


INSERT INTO LOAN (ts_now)
VALUES
('2020-11-28 12:12:12'),
('2020-12-28 14:23:51'),
('2021-01-28 08:56:22');

INSERT INTO BORROW_ITEM (n_book_id, n_loan_id)
VALUES
(1, 2),
(3, 2),
(2, 1),
(4, 3);


INSERT INTO WROTE(n_book_id, n_author_id)
VALUES
(1, 1),
(2, 1),
(2, 3),
(3, 3),
(4, 2);

