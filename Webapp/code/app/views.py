from flask import render_template, request, session
from pandas import DataFrame
import psycopg2
import random

from app.legerible import Legerible
from app import app

leg = Legerible()
app.secret_key = 'dljsawadslqk24e21cjn!Ew@@dsa5'


@app.route('/')  # Home
def index():
    count_total_books = leg.get_select("SELECT COUNT(DISTINCT(n_book_id)) FROM books").iat[0, 0]
    count_loaned_books = leg.get_select("SELECT COUNT(DISTINCT(n_loan_id)) FROM loan").iat[0, 0]

    result = leg.get_select(""" SELECT *
                                FROM(SELECT ROW_NUMBER() OVER (ORDER BY rp.Number_of_Loans DESC) AS TOP_Loans, rp.Book_ID, rp.ISBN, rp.Title, rp.Author_first_name, 
                                            rp.Author_last_name, rp.Number_of_Loans
                                    FROM(SELECT l.n_book_id AS Book_ID, b.s_isbn AS ISBN, b.s_title AS Title, 
                                                b.s_aut_first_name AS Author_first_name, b.s_aut_last_name AS Author_last_name,
                                                COUNT(l.n_book_id) AS Number_of_Loans
                                        FROM Loan AS L
                                            LEFT JOIN Books AS B ON L.n_book_id = B.n_book_id
                                        GROUP BY  l.n_book_id, b.s_isbn, b.s_title, b.s_aut_first_name, b.s_aut_last_name) AS rp
                                    ORDER BY rp.Number_of_Loans DESC) as r
                                WHERE r.TOP_Loans <=10""")

    return render_template("/index.html", amount_book_total=count_total_books,
                            amount_books_loaned=count_loaned_books, column_names=result.columns.values,
                               row_data=list(result.values.tolist()), link_column='none',zip=zip)


@app.route('/book')
def book():
    result = leg.get_select("""SELECT n_book_id, s_isbn AS ISBN, s_title AS Title, n_publishing_year AS Publishing_year, 
                                      s_book_language AS language,s_aut_first_name AS Author_first_name, 
                                      s_aut_last_name AS Author_last_name
                               FROM BOOKS""")
    return render_template("Books.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Books', link_column='none',
                               zip=zip)

@app.route('/loan_book', methods=['POST', 'GET'])
def loan_book():
    if request.method == 'POST':
        if request.form['do'] == 'Loan':
            result = leg.make_loan(int(request.form['book_id']))
        if result is True:
            return render_template("success.html", title='Success',
                                   text='Action executed successfully.')


@app.route('/generate_loan_book', methods=['POST', 'GET'])
def generate_loan_book():
    if request.method == 'POST':
        if request.form['do'] == 'Loan 50 Books automatically':
            count_total_books = leg.get_select("SELECT COUNT(DISTINCT(n_book_id)) FROM books").iat[0, 0]
            randomIDs = []
            for i in range(0,50):
                x = random.randint(1,count_total_books)
                randomIDs.append(x)
            result = leg.generate_loan(randomIDs)
        if result is True:
            return render_template("success.html", title='Success',
                                   text='Action executed successfully.')



@app.route('/loans', methods=['POST', 'GET'])
def loans():
    result = leg.get_select("""SELECT L.n_loan_id AS Loan_ID, L.ts_now as Timestamp, B.s_isbn AS ISBN, B.s_title AS Title, 
                                      B.s_aut_first_name AS Author_first_name, B.s_aut_last_name AS Author_last_name
                               FROM Loan AS L
                                    LEFT JOIN Books AS B ON (L.n_book_id = B.n_book_id)""")
    return render_template("Loans.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Loans', link_column='none',
                               zip=zip)



@app.route('/search_books', methods=['POST', 'GET'])
def search_books():
    text = request.form['search_text']
    result = leg.get_select(f"""SELECT n_book_id, s_isbn AS ISBN, s_title AS Title, n_publishing_year AS Publishing_year, 
                                      s_book_language AS language, s_aut_first_name AS Author_first_name, 
                                      s_aut_last_name AS Author_last_name 
                                FROM Books 
                                WHERE s_title LIKE '%{text}%'""")
    if isinstance(result, DataFrame):
        return render_template("Books.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Search', sub_header='Your search result', link_column='none',
                               zip=zip)
    else:
        return render_template("fail.html", title='Error',
                               text='No book found.')

@app.route('/search_loans', methods=['POST', 'GET'])
def search_loans():
    text = request.form['search_text']
    result = leg.get_select(f"""SELECT L.n_loan_id AS Loan_ID, L.ts_now as Timestamp, B.s_isbn AS ISBN, B.s_title AS Title, 
                                      B.s_aut_first_name AS Author_first_name, B.s_aut_last_name AS Author_last_name
                                FROM Loan AS L
                                    LEFT JOIN Books AS B ON (L.n_book_id = B.n_book_id)
                                WHERE s_title LIKE '%{text}%'""")
    if isinstance(result, DataFrame):
        return render_template("Loans.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Search', sub_header='Your search result', link_column='none',
                               zip=zip)
    else:
        return render_template("fail.html", title='Error',
                               text='No Loan found.')              

@app.route('/profile')  # Profile
def profile():
    active_user_id = session.get('user_id', None)
    if active_user_id is not None:

        return render_template("profile.html")
    else:
        return render_template("fail.html", title='Error',
                               text='You are not logged in!')

@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("login.html")

@app.route('/logged_in', methods=['POST', 'GET'])
def logged_in():
    session['user_id'] = leg.set_user(request.form['user_name'], request.form['password'])
    if session.get('user_id') is False:
        return render_template("fail.html", title='Failed Log-In',
                               text='You have not been logged in.')
    session['is_logged_in'] = 'logged_in'
    session['user_name'] = request.form['user_name']
    print(session.get('user_id', None))
    return render_template("success.html", title='Successful Login',
                           text='You have been successfully logged in.')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session['is_logged_in'] = 'logged_out'
    session['user_name'] = 'no name'
    session['user_id'] = None
    leg.s_user = None
    return render_template("success.html", title='Successful Logout',
                           text='You have been successfully logged out.')
