import random
import time

from flask import render_template, request, session
from flask_caching import *
from pandas import DataFrame

from app import app
from app import cache
from app.kafka_messaging import Producer
from app.legerible import Legerible

# from app.recommendation import recommandation

leg = Legerible()
kafka_producer = Producer()
app.secret_key = 'dljsawadslqk24e21cjn!Ew@@dsa5'


@app.context_processor
def logging_in():
    return dict(is_logged_in=session.get('is_logged_in', None),
                user=session.get('user_name', None),
                user_id=session.get('user_id', None))


@app.route('/')  # Home
@cache.cached(timeout=200)
def index():
    count_total_books = leg.get_select("SELECT COUNT(DISTINCT(n_book_id)) FROM books").iat[0, 0]
    count_loaned_books = leg.get_select("SELECT COUNT(DISTINCT(n_loan_id)) FROM loan").iat[0, 0]

    result = leg.get_select(""" SELECT *
                                FROM(SELECT ROW_NUMBER() OVER (ORDER BY rp.Number_of_Loans DESC) AS TOP_Loans, 
                                                                rp.Book_ID, rp.ISBN, rp.Title, rp.Author_first_name, 
                                                                rp.Author_last_name, rp.Number_of_Loans
                                    FROM(SELECT l.n_book_id AS Book_ID, b.s_isbn AS ISBN, b.s_title AS Title, 
                                                b.s_aut_first_name AS Author_first_name, 
                                                b.s_aut_last_name AS Author_last_name,
                                                COUNT(l.n_book_id) AS Number_of_Loans
                                        FROM Loan AS L
                                            LEFT JOIN Books AS B ON L.n_book_id = B.n_book_id
                                        GROUP BY  l.n_book_id, b.s_isbn, b.s_title, 
                                                    b.s_aut_first_name, b.s_aut_last_name) AS rp
                                    ORDER BY rp.Number_of_Loans DESC) as r
                                WHERE r.TOP_Loans <=10""")

    return render_template("/index.html", amount_book_total=count_total_books,
                           amount_books_loaned=count_loaned_books, column_names=result.columns.values,
                           row_data=list(result.values.tolist()), link_column='none', zip=zip)


@app.route('/book')
@cache.cached(timeout=500)
def book():
    active_user_id = session.get('user_id', None)
    if active_user_id is not None:
        result = leg.get_select("""SELECT n_book_id, s_isbn AS ISBN, s_title AS Title, 
                                          n_publishing_year AS Publishing_year, 
                                      s_book_language AS language,s_aut_first_name AS Author_first_name, 
                                      s_aut_last_name AS Author_last_name
                               FROM BOOKS""")
        return render_template("Books.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Books', link_column='none',
                               zip=zip)
    else:
        result = leg.get_select("""SELECT s_isbn AS ISBN, s_title AS Title, n_publishing_year AS Publishing_year, 
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
            user = session.get('user_id')
            result = leg.make_loan(int(request.form['book_id']), user)
        if result is True:
            # Generate Payload for Kafka Messaging - Dictionary with user_id and loaned book
            payload = {"user_id": user, "book_id": request.form['book_id'],
                       "timestamp": int(time.time())}

            # Send Payload via default producer
            kafka_producer.producer.send('book_stream_topic', value=payload). \
                add_callback(kafka_producer.on_success). \
                add_errback(kafka_producer.on_error)
            return render_template("success.html", title='Success',
                                   text='Action executed successfully.')


@app.route('/generate_loan_book', methods=['POST', 'GET'])
def generate_loan_book():
    if request.method == 'POST':
        if request.form['do'] == 'Loan 50 Books automatically':
            count_total_books = leg.get_select("SELECT COUNT(DISTINCT(n_book_id)) FROM books").iat[0, 0]
            randomIDs = []
            userIDs = []
            for i in range(0, 50):
                x = random.randint(1, count_total_books)
                randomIDs.append(x)
            active_user_id = session.get('user_id', None)

            if active_user_id is not None:
                user = session.get('user_id')
                for i in range(0, 50):
                    userIDs.append(user)
            else:
                count_total_users = leg.get_select("SELECT COUNT(DISTINCT(n_user_id)) FROM users").iat[0, 0]
                for i in range(0, 50):
                    x = random.randint(1, count_total_users)
                    userIDs.append(x)

            result = leg.generate_loan(randomIDs, userIDs, kafka_producer)
        if result is True:
            return render_template("success.html", title='Success',
                                   text='Action executed successfully.')


@app.route('/loans', methods=['POST', 'GET'])
@cache.cached(timeout=20)
def loans():
    result = leg.get_select("""SELECT L.n_loan_id AS Loan_ID, L.ts_now as Timestamp, 
                                      B.s_isbn AS ISBN, B.s_title AS Title, 
                                      B.s_aut_first_name AS Author_first_name, B.s_aut_last_name AS Author_last_name, 
                                      U.s_user_name AS User
                               FROM Loan AS L
                                    LEFT JOIN Books AS B ON (L.n_book_id = B.n_book_id)
                                    LEFT JOIN Users AS U ON (L.n_user_id = U.n_user_id)""")
    return render_template("Loans.html", column_names=result.columns.values,
                           row_data=list(result.values.tolist()),
                           title='Loans', link_column='none',
                           zip=zip)


@app.route('/search_books', methods=['POST', 'GET'])
def search_books():
    text = request.form['search_text']
    result = leg.get_select(f"""SELECT n_book_id, s_isbn AS ISBN, s_title AS Title, 
                                      n_publishing_year AS Publishing_year, 
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
    result = leg.get_select(f"""SELECT L.n_loan_id AS Loan_ID, L.ts_now as Timestamp, B.s_isbn AS ISBN, 
                                       B.s_title AS Title, 
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


@app.route('/profile', methods=['POST', 'GET'])  # Profile
@cache.cached(timeout=300)
def profile():
    active_user_id = session.get('user_id', None)
    if active_user_id is not None:
        user = session.get('user_name')
        result = leg.get_select(f"""SELECT s_first_name, s_last_name,n_user_id
                                        FROM Users
                                        WHERE s_user_name LIKE '%{user}%'""")

        result1 = leg.get_select(f"""SELECT L.ts_now as Timestamp, B.s_isbn AS ISBN, B.s_title AS Title,
                                        B.s_aut_first_name AS Author_first_name, B.s_aut_last_name AS Author_last_name
                                    FROM Loan AS L
                                        LEFT JOIN Books AS B ON (L.n_book_id = B.n_book_id)
                                        LEFT JOIN Users AS U ON (L.n_user_id = U.n_user_id)
                                    WHERE U.s_user_name LIKE '%{user}%'""")

        result3 = ""  # recommandation(result1)

        return render_template("profile.html", user=user, column_names=result.columns.values,
                               row_data=list(result.values.tolist()), link_column='none', zip=zip,
                               column_names1=result1.columns.values,
                               row_data1=list(result1.values.tolist()),
                               link_column1='none',
                               zip1=zip, result3=result3)
    else:
        return render_template("fail.html", title='Error',
                               text='You are not logged in!')

@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("login.html")


@app.route('/logged_in', methods=['POST', 'GET'])
def logged_in():
    user_id = leg.set_user(request.form['user_name'], request.form['password'])
    cache.clear()
    if user_id is False:
        session['user_id'] = user_id
        session['is_logged_in'] = 'logged_out'
        session['user_id'] = None
        return render_template("fail.html", title='Failed Log-In',
                               text='You have not been logged in.')

    else:
        session['user_id'] = user_id
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
    cache.clear()
    return render_template("success.html", title='Successful Logout',
                           text='You have been successfully logged out.')
