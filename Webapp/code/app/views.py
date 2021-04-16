from flask import render_template, request, session
from pandas import DataFrame
import psycopg2

from app.selections import Selections
from app.biblio import Biblio
from app.book import Book
from app import app

bib = Biblio()
app.secret_key = 'dljsawadslqk24e21cjn!Ew@@dsa5'

@app.route('/')  # Home
def index():
    # fetch amount of books currently overdue
    count_loaned_books = bib.get_select("""SELECT COUNT(DISTINCT (n_borrow_item_id)) AS Amount
                                               FROM borrow_item AS bi
                                                    LEFT JOIN loan AS l ON bi.n_loan_id = l.n_loan_id
                                               WHERE bi.b_active = 'TRUE'""").iat[0, 0]
    count_total_books = bib.get_select("SELECT COUNT(DISTINCT(n_book_id)) FROM books").iat[0, 0]

    return render_template("/index.html", amount_book_total=count_total_books,
                           amount_books_loaned=count_loaned_books)
    # return render_template("/index.html", user=session.get('user_name'))


@app.route('/search', methods=['POST', 'GET'])
def search():
    text = request.form['search_text']
    result = bib.get_select(f"SELECT * FROM book_extended WHERE s_title LIKE '%{text}%'")
    if isinstance(result, DataFrame):
        return render_template("includes/table.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Search', sub_header='Your search result', link_column='none',
                               zip=zip)
    else:
        return render_template("includes/fail.html", title='Error',
                               text='No book found.')


@app.route('/book')
def book():
    result = bib.get_select("SELECT * FROM book_extended")
    result = result.drop_duplicates(subset=["n_book_id"], keep='last')  # better visualisation
    if isinstance(result, DataFrame):
        return render_template("includes/table.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Books', sub_header='List of all your books', link_column='none',
                               zip=zip)
    else:
        return render_template("includes/fail.html", title='Error',
                               text='Site could not be loaded.')


@app.route('/loan_or_read_book', methods=['POST', 'GET'])
def loan_or_read_book():
    if request.method == 'POST':
        if request.form['do'] == 'Loan':
            result = bib.make_loan(int(request.form['book_id']))
        if result is True:
            return render_template("includes/success.html", title='Success',
                                   text='Action executed successfully.')
    return render_template("includes/fail.html", title='Error',
                           text='Something went wrong.')


@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
    return render_template("add_book.html")


@app.route('/execute_add_book', methods=['POST', 'GET'])
def execute_add_book():
    new_book = Book()
    new_book.set_via_isbn(request.form['book_isbn'])
    result = bib.add_new_book(new_book)
    if result is True:
        return render_template("includes/success.html", title='New book added',
                               text='You have add a new book successfully.')
    return render_template("includes/fail.html", title='No book added',
                           text='You have not added the book.')


@app.route('/execute_add_book_manually', methods=['POST', 'GET'])
def execute_add_book_manually():
    new_book = Book()
    edition = request.form['book_edition']
    if edition == "":
        edition = 1
    param_list = [request.form['author_first_names'],
                  request.form['author_last_names'],
                  request.form['publisher_name'],
                  request.form['book_title'],
                  edition,
                  request.form['book_language'],
                  request.form['book_genre'],
                  request.form['book_isbn'],
                  request.form['publishing_year'],
                  request.form['location_id'],
                  request.form['reco_age']]
    final_list = list()
    for param in param_list:
        if param == "":
            param = None
        final_list.append(param)
    new_book.set_manually(final_list)
    result = bib.add_new_book(new_book)
    if result is True:
        return render_template("includes/success.html", title='New book added',
                               text='You have add a new book successfully.')
    return render_template("includes/fail.html", title='No book added',
                           text='You have not added the book.')


@app.route('/active_loans', methods=['POST', 'GET'])
def active_loans():
    result = bib.get_select(Selections.sql_user_active_loans(session.get('user_id', None)))
    print(request)
    if isinstance(result, DataFrame):
        return render_template("includes/table.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Loans', sub_header='List of all your active loans', link_column='none',
                               zip=zip)
    else:
        return render_template("includes/fail.html", title='Error',
                               text='Site could not be loaded.')




########################################################################################################################
# Update / Delete Pages

@app.route('/update_book', methods=['POST', 'GET'])
def update_book():
    df_book = bib.get_select("SELECT * FROM books ORDER BY n_book_id ASC")
    return render_template("update_book.html",
                           column_names=df_book.columns.values, row_data=list(df_book.values.tolist()), zip=zip)


@app.route('/execute_change_book_manually', methods=['POST', 'GET'])
def execute_change_book_manually():
    new_book = Book()

    # Determine book_id for future operations
    # if Edition is not known it will default to 1
    book_edition = request.form['book_edition']
    if book_edition == "":
        book_edition = 1

    # fetch title to use for checks
    book_title = request.form['book_title']

    # check how to determine the book_id
    # cannot determine which book if title is not present
    if book_title == "":
        return render_template("includes/fail.html", title='Transaction failed',
                               text='Transaction failed! Reason: Missing book identifier.')
    elif book_title != "":
        try:
            book_id = bib.get_select(f"""SELECT n_book_id FROM books 
                                         WHERE s_title = '{book_title}'  AND n_book_edition = {book_edition}""").iat[
                0, 0]
        except IndexError:
            return render_template("includes/fail.html", title="Transaction failed",
                                   text=f"Transaction failed! Reason: Book cannot be found or does it not exist?")

    # Operation defined by radio button in form
    if request.form['operator'] == "delete":

        try:
            bib.exec_statement(f"""DELETE FROM books WHERE n_book_id = {book_id};""")
        except psycopg2.errors.ForeignKeyViolation:
            return render_template("includes/fail.html", title='Book deletion failed',
                                   text='Delete failed! Reason: Book id cannot be deleted because of table constraints.')
        except psycopg2.errors.InFailedSqlTransaction:
            return render_template("includes/fail.html", title='Book deletion failed',
                                   text='Delete failed! Reason: Book does not exist.')
        except Exception as err:
            return render_template("includes/fail.html", title="Book deletion failed",
                                   text=f"Delete failed! Reason {err}")
        else:
            return render_template("includes/success.html", title='Book deleted',
                                   text='Book was successfully deleted.')
    else:
        param_list = [
            book_edition,
            request.form['book_language'],
            request.form['book_genre'],
            request.form['publishing_year'],
            request.form['location_id'],
            request.form['reco_age'],
            request.form['book_isbn'],
            book_title]

        result = list()
        for item in param_list:
            if item == "":
                result.append(None)
            else:
                result.append(item)

        result = bib.exec_statement(f'''UPDATE books
                                        SET (n_book_edition, s_genre, n_publishing_year,
                                            s_book_language, n_recommended_age, n_location_id, s_isbn) =
                                            ({result[0]}, '{result[2]}', {result[3]},
                                             '{result[1]}', {result[5]}, {result[4]}, {result[6]})
                                        WHERE n_book_id = {book_id};'''.replace("'None'", "NULL").replace("None",
                                                                                                          "NULL"))

        if result is True:
            return render_template("includes/success.html", title='Book updated',
                                   text='Book updated successfully')
            return render_template("includes/fail.html", title='Book update failed',
                                   text='You have not updated the book.')

###########################################################################


@app.route('/dev', methods=['POST', 'GET'])  # Testing
def dev():
    return render_template("_dev.html")
