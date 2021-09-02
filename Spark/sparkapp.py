from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import numpy as np
import pandas as pd
import pyspark.sql.functions as F
from pyspark.sql.types import DoubleType
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from Webapp.code.app.legerible import Legerible
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.mllib.feature import HashingTF, IDF

leg = Legerible()

all_loans = leg.get_select("""SELECT L.n_loan_id AS Loan_ID, L.ts_now as Timestamp, B.s_isbn AS ISBN, B.s_title AS Title, 
                                  B.s_aut_first_name AS Author_first_name, B.s_aut_last_name AS Author_last_name, U.s_user_name AS User
                               FROM Loan AS L
                                      LEFT JOIN Books AS B ON (L.n_book_id = B.n_book_id)
                                      LEFT JOIN Users AS U ON (L.n_user_id = U.n_user_id)""")

sc = SparkSession.builder.appName("spark-app").master("local[*]").getOrCreate()
sparkContext = sc.sparkContext
lines = sc.read.csv("isbn.txt")

def count_books(self):
    return self.distinct().count()

top_x = all_loans.groupby("books_id").count()
count_b = count_books(lines)
count_l = count_books(all_loans)

def return_counts():
    a = []
    a.append(count_b)
    a.append(count_l)
    a.append(top_x)
    return a
leg = Legerible()

def recommendation(user_id):
    #getting all loaned books by the user
    loans = leg.get_selectt(f"""SELECT L.ts_now as Timestamp, B.s_isbn AS ISBN, B.s_title AS Title,
                                        B.s_aut_first_name AS Author_first_name, B.s_aut_last_name AS Author_last_name
                                    FROM Loan AS L
                                        LEFT JOIN Books AS B ON (L.n_book_id = B.n_book_id)
                                        LEFT JOIN Users AS U ON (L.n_user_id = U.n_user_id)
                                    WHERE U.s_user_name LIKE '%{user_id}%'""")
    # getting books and loaned books from db
    books_loans = leg.get_select("""SELECT n_book_id, s_isbn AS ISBN, s_title AS Title, n_publishing_year AS Publishing_year, 
                                      s_book_language AS language,s_aut_first_name AS Author_first_name, 
                                      s_aut_last_name AS Author_last_name
                                   FROM BOOKS""")

    #getting last loaned book
    expr = [F.last(col).alias(col) for col in loans.columns]
    last_loaned = loans.agg(*expr).select("book_id").collect()[0][-1]

    # function to get all important attributes
    df = books_loans.withColumn("important_features", concat_ws(",", "isbn", 'title', 'language'))

    # Bringing the important_features into the RDD Form
    rdd = sparkContext.parallelize(
        [[0, '9780575097568, Rivers of London,en'], [1, '9780345524591, Moon Over Soho,None'],
         [2, '9780525516019, A Land of Permanent Goodbyes,en'], [3, 'None,Der Text des Lebens,de'],
         [4, '9783453273351, Später,un'], [5, '9783492070904, Das Geheimnis von Zimmer 622 - Roman,un'],
         [6, '9783257071481, Hard Land,un'], [7, '9783785727416, Der neunte Arm des Oktopus - Thriller,un'],
         [8, '9783455011784, The Hill We Climb: Ein Gedicht zur Inauguration,un'],
         [9, '9783423282789, Vom Aufstehen - Ein Leben in Geschichten,un'],
         [10, '9783423282734, Junge Frau, am Fenster stehend, Abendlicht, blaues Kleid - Roman,un'],
         [11, '9783630876672, Über Menschen - Roman,un'], [12, '9783426282564, Die Mitternachtsbibliothek - Roman,un'],
         [13, '9783446269156, Sprich mit mir - Roman,un'], [14, '9783866124776, Der Buchspazierer - Roman,un'],
         [15, '9783764510473, Der Fall des Präsidenten - Thriller,un'],
         [16, '9783832181536, Der große Sommer - Roman,un'], [17, '9783737101127, Monschau,un'],
         [18, '9783426281550, Der Heimweg,un'], [19, '9783462050837, Eurotrash - Roman,un'],
         [20, '9783462053289, Kim Jiyoung, geboren 1982 - Roman,un'],
         [21, '9783896676931, Klara und die Sonne - Roman,un'],
         [22, '9783442316397, Von der Pflicht - Eine Betrachtung,un'], [23, '9783103973150, Adas Raum - Roman,un'],
         [24, '9783833877179, Genesis - Die Befreiung der Geschlechter,un'],
         [25, '9783462053616, Komplett Gänsehaut,un'], [26, '9783462054767, Der Mann im roten Rock,un'],
         [27, '9783492075008, Und erlöse uns von den Blöden - Vom Menschenverstand in hysterischen Zeiten,un'],
         [28, '9783965840928, Die Ernährungs-Docs - Gesund und schlank durch Intervallfasten,un'],
         [29, '9783861221265, Die fünf Sprachen der Liebe - wie Kommunikation in der Ehe gelingt,un'],
         [30, '9783827501530, Der Wahrheit verpflichtet - Meine Geschichte,un'],
         [31, '9783948319007, ON/ OFF GESUNDHEIT - Den Körper neu erschaffen durch Ernährung,un'],
         [32, '9783789129407, Ronja Räubertochter,un'], [33, '9783751200530, Dunkelnacht,un']])

    # Compute TF-IDF
    documents = rdd.map(lambda l: l[1].replace(" ", "").split(","))

    from pyspark.mllib.feature import HashingTF, IDF
    hashingTF = HashingTF()
    tf = hashingTF.transform(documents)

    tf.cache()
    idf = IDF().fit(tf)
    tfidf = idf.transform(tf)

    # Compute L2 norm
    from pyspark.mllib.feature import Normalizer
    labels = rdd.map(lambda l: l[0])
    features = tfidf

    normalizer = Normalizer()
    data = labels.zip(normalizer.transform(features))

    # Compute cosine similarity by multiplying the matrix with itself
    from pyspark.mllib.linalg.distributed import IndexedRowMatrix
    mat = IndexedRowMatrix(data).toBlockMatrix()
    dot = mat.multiply(mat.transpose())
    dot.toLocalMatrix().toArray()

    data.cartesian(data) \
        .map(lambda l: ((l[0][0], l[1][0]), l[0][1].dot(l[1][1]))) \
        .sortByKey() \
        .collect()

    import pyspark.sql.functions as psf
    #creating model
    df = rdd.toDF(["ID", "Office_Loc"]) \
        .withColumn("Office_Loc", psf.split(psf.regexp_replace("Office_Loc", " ", ""), ','))

    from pyspark.ml.feature import HashingTF, IDF
    hashingTF = HashingTF(inputCol="Office_Loc", outputCol="tf")
    tf = hashingTF.transform(df)

    #fitting data into model
    idf = IDF(inputCol="tf", outputCol="feature").fit(tf)
    tfidf = idf.transform(tf)

    from pyspark.ml.feature import Normalizer
    #normilize feautures
    normalizer = Normalizer(inputCol="feature", outputCol="norm")
    data = normalizer.transform(tfidf)

    dot_udf = psf.udf(lambda x, y: float(x.dot(y)), DoubleType())

    #creating recommendation dataframe
    rec_df= data.alias("loaned_book").join(data.alias("book_id"), psf.col("loaned_book.ID") < psf.col("book_id.ID"))
    #calculating the score point between last loaned book and all books
    rec_df = rec_df.select(psf.col("loaned_book.ID").alias("loaned_book"), psf.col("book_id.ID").alias("book_id"), dot_udf("loaned_book.norm", "book_id.norm").alias("Score"))
    rec_df = rec_df.filter(F.col('loaned_book') == last_loaned).sort(col('Score').desc())

    result = []
    for i in range(0, 4):
        result.append(rec_df.select('book_id').collect()[i][0])
        
    #returning result in form of array with top4 recommendation book_id
    return result

