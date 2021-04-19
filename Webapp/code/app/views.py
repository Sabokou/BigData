from flask import render_template, request, session
from pandas import DataFrame
import psycopg2

from app.biblio import Biblio
from app import app

bib = Biblio()
app.secret_key = 'dljsawadslqk24e21cjn!Ew@@dsa5'

@app.route('/')  # Home
def index():
    count_loaned_books = bib.get_select("""SELECT COUNT(DISTINCT (n_borrow_item_id)) AS Amount
                                               FROM borrow_item AS bi
                                                    LEFT JOIN loan AS l ON bi.n_loan_id = l.n_loan_id
                                               WHERE bi.b_active = 'TRUE'""").iat[0, 0]
    count_total_books = bib.get_select("SELECT COUNT(DISTINCT(n_book_id)) FROM books").iat[0, 0]

    return render_template("/index.html", amount_book_total=count_total_books,
                           amount_books_loaned=count_loaned_books)


@app.route('/book')
def book():
    result = bib.get_select("SELECT * FROM book_extended")
    result = result.drop_duplicates(subset=["n_book_id"], keep='last')  # better visualisation
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
    result = bib.get_select("SELECT * FROM book_extended WHERE b_is_available = False")
    print(request)
    if isinstance(result, DataFrame):
        return render_template("table.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Loans', link_column='none',
                               zip=zip)
    else:
        return render_template("fail.html", title='Error',
                               text='Site could not be loaded.')



