import numpy as np
import pandas as pd
import psycopg2
import time
import datetime
import sys
from constants import DB_NAME, DB_HOST, DB_PASS, DB_PORT, DB_USER, DB_TIME

news = sys.argv[1]
news_insert_template = """
INSERT INTO news(title,link,deleted)
VALUES({title},{link},{deleted});
"""
commnets_insert_template = """
INSERT INTO comments(content,likes,dislikes,reply_to,news_id,deleted)
VALUES({content},{likes},{dislikes},{reply_to},{news_id},{deleted});
"""
def init_db_connection():
    today = datetime.datetime.now()

    try:  # connect to postgres
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            host=DB_HOST,
            port=DB_PORT,
            password=DB_PASS,
            connect_timeout=DB_TIME
        )
        tm = time.time()
        return conn
        print('Connected to database: [%s] @ %d seconds' %
            (DB_HOST, time.time() - tm))
    except Exception as e:
        print('Cannot connect to Postgres [%s]' % DB_HOST)
        print(str(e))
        exit(1)


#conn = init_db_connection()

col_names = ['id',
             'content',
             'likes',
             'dislikes',
             'reply_to',
             'news_id',
             'news_title',
             'news_link']
data = pd.read_csv('./collected-data/{}-comments.csv'.format(news),sep=';',names=col_names)

news_data = data['news_id','news_title','news_link']
print(news_data.head())

