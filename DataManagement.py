from datetime import date
import time
import os
import sqlite3
import sys
from custom_excpetions import *


data_base_path = r'C:\Users\mclau\Selenium-Tut\post.db'
#Add post info to sqlite database table. Initialize Database and tables if it does not already exist
def insertPost(post_path,caption,genre,hashtags,status,date,file_type):
    postDB_ini()
       
            
    post_database = sqlite3.connect('post.db')
    post_database.execute('''INSERT INTO CONTENT (PATH, CAPTION, GENRE, SOURCE_TAGS, POST_STATUS, Download_Date, File_Type)
                                VALUES (?,?,?,?,?,?,?);''', (post_path,caption,genre,hashtags,status,date,file_type))
    post_database.commit()
    post_database.close()
   
#get top row from content table, detlete it from the content table and place it in the posted table
def get_post_data():
    try:
        todays_date = date.today()
        post_database = sqlite3.connect('post.db')
        cursor = post_database.cursor()
        cursor.execute('''SELECT * FROM CONTENT ORDER BY ID LIMIT 1''') #Limit first row to the number 1 id
        top_row = cursor.fetchone() #list with first row contents
        row_list = list(top_row) #Change tuple to list so that i can change values
        row_list[6] = todays_date
        row_list[5] = True
        top_row = tuple(row_list) #change list back to tuple so it can be added to SQL table
        cursor.execute('''INSERT INTO POSTED
                              VALUES(?,?,?,?,?,?,?,?)''',top_row)
        cursor.execute('DELETE FROM CONTENT WHERE ID =?', (top_row[0],))
        post_database.commit()
        post_database.close()
        
        return top_row
      
    except Exception as e:
        print('Sql Error: ' +str(e))


#==============File Io functions===================#

#find latest file name for sql table

def get_file_name(directory_string):
     file_list = os.listdir(directory_string)
     if not file_list:
          return("Waddup Loser. No files here.")
     
     file_list.sort(key = (lambda x : os.path.getmtime(os.path.join(directory_string,x))), reverse = True)

     return(file_list[0])

def isEmptyTable(data_base,table_name):
    cursor = data_base.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    row_list = cursor.fetchall()
    if len(row_list) == 0:
        raise emptySQLTableException()
    
def postDB_ini():
    try:
            post_database = sqlite3.connect('post.db')
                    
            post_database.execute('''CREATE TABLE CONTENT
                                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    PATH  TEXT,
                                    CAPTION TEXT,
                                    GENRE TEXT,
                                    SOURCE_TAGS TEXT,
                                    POST_STATUS TEXT,
                                    Download_Date DATE,
                                    File_Type TEXT);
                                    ''')
            post_database.execute('''CREATE TABLE POSTED
                                        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        PATH TEXT,
                                        CAPTION TEXT,
                                        GENRE TEXT,
                                        SOURVE_TAGS TEXT,
                                        POST_STATUS,
                                        POST_DATE DATE,
                                        File_Type TEXT);
                                        ''')
    except Exception as e:
            print(str(e))




