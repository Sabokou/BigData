import numpy as np
import pandas as pd
import collections
import copy
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from app.legerible import Legerible

leg = Legerible()

def recommandation(user_loans):
       #getting books and loaned books from db
       books = leg.get_select("""SELECT n_book_id, s_isbn AS ISBN, s_title AS Title, n_publishing_year AS Publishing_year, 
                                      s_book_language AS language,s_aut_first_name AS Author_first_name, 
                                      s_aut_last_name AS Author_last_name
                                   FROM BOOKS""")

       loans = leg.get_select("""SELECT L.n_loan_id AS Loan_ID, L.ts_now as Timestamp, B.s_isbn AS ISBN, B.s_title AS Title, 
                                      B.s_aut_first_name AS Author_first_name, B.s_aut_last_name AS Author_last_name, U.s_user_name AS User
                                   FROM Loan AS L
                                          LEFT JOIN Books AS B ON (L.n_book_id = B.n_book_id)
                                          LEFT JOIN Users AS U ON (L.n_user_id = U.n_user_id)""")

       #convertring variables to strings
       loans["isbn"] = loans["isbn"].astype(str)
       loans_list = loans['isbn'].tolist()
       books_loans = books
       books_loans["isbn"] = books_loans["isbn"].astype(str)
       books_loans["title"] = books_loans["title"].astype(str)
       books_loans["language"] = books_loans["language"].astype(str)
       books_loans["author_first_name"] = books_loans["author_first_name"].astype(str)
       books_loans["author_last_name"] = books_loans["author_last_name"].astype(str)
       books_loans["isbn"] = books_loans["isbn"].astype(str)
       books_loans['loaned'] = books_loans['isbn'].isin(loans_list)
       books_loans["loaned"] = books_loans["loaned"].astype(str)
       books_loans["books_id"] = books_loans.index
       user_loans["title"] = user_loans["title"].astype(str)

       #function to get all important attributes
       def get_important_features(data):
              important_features= []
              for i in range(0, data.shape[0]):
                     important_features.append(data["isbn"][i]+' '+data["title"][i]+' '+data["language"][i]+' '+data["loaned"][i])  
    
              return important_features

       books_loans["important_features"] = get_important_features(books_loans)
       
       #pitting model for cosinus simularity score calculation 
       cm = CountVectorizer().fit_transform(books_loans["important_features"])
       cs = cosine_similarity(cm)

       def top_rec(title, j=0):
              #calculating scores for all books
              book_id =  books_loans[books_loans.title==title]["books_id"].values[0]
              scores = list(enumerate(cs[book_id]))

              sorted_scores = sorted(scores, key = lambda x:x[1], reverse=True)
              sorted_scores = sorted_scores[1:]

              #adding top books to array
              all_books = []
              print("The 4 Most recommended books for you, because you liked" + title+ "are:\n")
              for item in sorted_scores:
                     book_title =  books_loans[books_loans.books_id==item[0]]["title"].values[0]
                     print(j+1, book_title)
                     j = j+1
                     all_books.append(book_title)
                     if j>=4:
                            break
              return all_books

       #calculating 4 recommendations for each loaned book
       top_books=[]
       processed_books = []
       for i in user_loans["title"]:
              #checking wether recommendations 
              if i in processed_books:
                     pass
              else: 
                     top_books.append(top_rec(i))
              processed_books.append(i)

       #converting array of recommendation arrays to single array
       total_rec = []
       for i in top_books:
              for processed_books in i:
                     total_rec.append(processed_books)

       #calculating count of each book in array
       book_count = collections.Counter(total_rec)

       #variable to be able to delete variables from dictionary while iterating through it
       count_weg = copy.deepcopy(book_count)

       #deleting recommended books that have already been loaned
       for key in count_weg:
              if str(key) in str(user_loans["title"]):
                     book_count.pop(key)
       
       final_recommendation = sorted(book_count, key=book_count.get, reverse=True)[:4]
       
       return final_recommendation