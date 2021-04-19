from flask import render_template, request, session
from pandas import DataFrame
import psycopg2

from app.biblio import Biblio
from app import app

bib = Biblio()
app.secret_key = 'dljsawadslqk24e21cjn!Ew@@dsa5'

@app.route('/')  # Home
def index():
    count_total_books = bib.get_select("SELECT COUNT(DISTINCT(n_book_id)) FROM books").iat[0, 0]
    count_loaned_books = bib.get_select("SELECT COUNT(DISTINCT(n_loan_id)) FROM loan").iat[0, 0]

    result = bib.get_select(""" SELECT ROW_NUMBER() OVER (ORDER BY rp.Number_of_Loans DESC) AS TOP_Loans, rp.Book_ID, rp.ISBN, rp.Title, rp.Author_first_name, 
                                        rp.Author_last_name, rp.Number_of_Loans
                                FROM(SELECT l.n_book_id AS Book_ID, b.s_isbn AS ISBN, b.s_title AS Title, 
                                            b.s_aut_first_name AS Author_first_name, b.s_aut_last_name AS Author_last_name,
                                            COUNT(l.n_book_id) AS Number_of_Loans,
                                            rank()
                                            OVER (PARTITION BY l.n_book_id, b.s_isbn, b.s_title, b.s_aut_first_name, b.s_aut_last_name 
                                                    ORDER BY COUNT(l.n_book_id)DESC)
                                    FROM Loan AS L
                                        LEFT JOIN Books AS B ON L.n_book_id = B.n_book_id
                                    GROUP BY  l.n_book_id, b.s_isbn, b.s_title, b.s_aut_first_name, b.s_aut_last_name) AS rp
                                WHERE rank <=10
                                ORDER BY rp.Number_of_Loans DESC;""")

    return render_template("/index.html", amount_book_total=count_total_books,
                            amount_books_loaned=count_loaned_books, column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Loans', link_column='none',
                               zip=zip)


@app.route('/book')
def book():
    result = bib.get_select("""SELECT n_book_id, s_isbn AS ISBN, s_title AS Title, n_publishing_year AS Publishing_year, 
                                      s_book_language AS language, n_recommended_age AS age,
                                      s_aut_first_name AS Author_first_name, s_aut_last_name AS Author_last_name
                               FROM BOOKS""")
    if isinstance(result, DataFrame):
        return render_template("table.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Books', link_column='none',
                               zip=zip)
    else:
        return render_template("fail.html", title='Error',
                               text='Site could not be loaded.')

@app.route('/loan_book', methods=['POST', 'GET'])
def loan_book():
    if request.method == 'POST':
        if request.form['do'] == 'Loan':
            result = bib.make_loan(int(request.form['book_id']))
        if result is True:
            return render_template("success.html", title='Success',
                                   text='Action executed successfully.')
    return render_template("fail.html", title='Error',
                           text='Something went wrong.')



@app.route('/loans', methods=['POST', 'GET'])
def loans():
    result = bib.get_select("""SELECT L.n_loan_id AS Loan_ID, L.ts_now as Timestamp, B.s_isbn AS ISBN, B.s_title AS Title, 
                                      B.s_aut_first_name AS Author_first_name, B.s_aut_last_name AS Author_last_name
                               FROM Loan AS L
                                    LEFT JOIN Books AS B ON (L.n_book_id = B.n_book_id)""")
    print(request)
    if isinstance(result, DataFrame):
        return render_template("table.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Loans', link_column='none',
                               zip=zip)
    else:
        return render_template("fail.html", title='Error',
                               text='Site could not be loaded.')



