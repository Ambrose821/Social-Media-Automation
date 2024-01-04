from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import DataManagement
import sqlite3

from instabot import Bot
import os 
import glob

import shutil
from tiktok_uploader.upload import upload_video, upload_videos






class post:


    


    def __init__(self,title,path,genre):
        post.post_id +=1
        self.title_String = title
        self.content_path = path 
        print("Default Platform set to Twitter")
        self.sm_platform = 'https://twitter.com/'

    #IMPORTANT IDEA CHANGE POST STATUS IN SQL TABLE TO A COUNTER WHICH INCREMENTS FOR EACH ACCOUNT ITS BEEN POSTED ON. IF ITS REACHES 4 FOR EXAMPLE IT GETS SENT TO POSTED. FOR TWITTER YOU CAN GET ALL WHERE COUNT  = 0 FOR EXAMPLE AND FOR INSTA WHERE COUNT =1

    def insta_post(num_posts = 10):
        cookie_del = glob.glob("config/*cookie.json")
        os.remove(cookie_del[0])
        #====== SQL Biz ============
        DataManagement.postDB_ini
        table_name = "CONTENT"
        post_database = sqlite3.connect('post.db')
        post_info = DataManagement.get_post_data()

        DataManagement.isEmptyTable(post_database,table_name)
        
        #==============Insta Biz======================
        bot = Bot()
        
        
        bot.login(username ='shuffle_media', password='matamb123')

        
        path = post_info[1]
        if path.endswith(".crdownload"):
            path = path[0:-11]
        print(path)
        basic_caption = post_info[2]
        tags = "\n" + post_info[4]
        insta_caption = basic_caption + tags

        if path.endswith(".mp4"):
            bot.upload_video(path,caption = insta_caption)
        else:
            bot.upload_photo(path,insta_caption)
        
    
        

    def tik_tok_post(num_posts = 10):
        DataManagement.postDB_ini
        post_database = sqlite3.connect('post.db')
        post_database.execute('''SELECT * FROM CONTENT WHERE File_Type = "video";''')
        table_name = "CONTENT"
        DataManagement.isEmptyTable(post_database,table_name)

        options =ChromeOptions()
        options.add_experimental_option("detach",True)
        driver = webdriver.Chrome(options = options)
        action = ActionChains(driver)
        load_wait = WebDriverWait(driver,180)

        driver.get('https://www.tiktok.com/login/phone-or-email/email')

        upload_btn = load_wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="app-header"]/div/div[3]/div[1]/a')))

        upload_btn.click()

        file_input = load_wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="root"]/div/div/div/div/div/div/div/input')))

        
        post_info = DataManagement.get_post_data()
        
        path = post_info[1]
        print(path)
        basic_caption = post_info[2]
        tags = "\n" + post_info[4]

        caption = basic_caption + tags

        print(caption)
        
        file_input.send_keys(path)
        

        
        






    


        
        #=========FOURTH PAGE===============
    def send_post_twitter(num_posts = 10):
        DataManagement.postDB_ini()
        post_database = sqlite3.connect('post.db')
        table_name = "CONTENT"
        DataManagement.isEmptyTable(post_database,table_name)
        
        options =ChromeOptions()
        options.add_experimental_option("detach",True)
        driver = webdriver.Chrome(options = options)
        driver.get('https://twitter.com/')
        
        action = ActionChains(driver)

        load_wait = WebDriverWait(driver,60)

        sign_in_btn = load_wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[5]/a')))
        
        sign_in_btn.click()

        time.sleep(2)


        user_name = load_wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')))
        user_name.click()
        user_name.send_keys("ShuffleContent")
        

        next_button = load_wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]')))

        next_button.click()
        password = load_wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')))
        password.click()
        password.send_keys('ambmat123')
        time.sleep(2)
        login_btn = load_wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')))

        login_btn.click()

        for x in range(num_posts):
       
            post_btn = load_wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a')))
            post_btn.click()

            textbox = load_wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div[2]/div/div/div/div')))

            post_info = DataManagement.get_post_data()
            path = post_info[1]
            if path.endswith(".crdownload"):
                path = path[0:-11]
            print(path)
            if path.endswith(".tmp"):
                print("Skipping a post due to tmp")
                continue
            basic_caption = post_info[2]
            tags = "\n" + post_info[4]
            textbox.click()
            caption = basic_caption + tags
            if len(caption) > 279:
                continue
            textbox.send_keys(caption)
        

            #========================File Upload=============================

        
            time.sleep(0.5)
            secret_input = load_wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input')))
           
            time.sleep(.5)
        
            try:
                secret_input.send_keys(path)
            except Exception as e:
                print("------------------------Erorr: " + str(e)+"-------------------------------")
            
            
            time.sleep(15)
            post_btn = driver.find_element(By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div[2]/div[4]')
            try:
                post_btn.click()
            except:
                time.sleep(15)
                post_btn.click()




    
    


    
        