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
from datetime import date
import time
import os
import sqlite3
import sys
import DataManagement

class Sourcer:
        
    #Browser options
    


    default_directory = r'C:\Users\mclau\Selenium-Tut\post_downloads'
    #set options parameter to your option

    def __init__(self, download_directory=default_directory): 
        self.download_dir = download_directory
        prefs = {'download.default_directory': self.download_dir}
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)  # Assign to self.driver

        # Create Hover Element for testing
        self.action = ActionChains(self.driver)  # Initialize self.action
        self.load_wait = WebDriverWait(self.driver, 60)  # Initialize self.load_wait
    
    def get_top_content(self,search_genre = 'meme', number_of_posts = 10):
        self.driver.get("https://9gag.com/top")
         
        try:
            self.driver.find_element_by_xpath('//*[@id="jsid-app"]/div/div[2]/div/div[1]/div/div[1]/div/svg').click()
            print("Closed Pop-up")
        except:
            print("No Pop Up this time")
            height = self.driver.execute_script('return document.body.scrollHeight')

        print("height :" + str(height))


        #Use this function to make sure page is loaded
        def wait_for_page():
            return self.driver.execute_script("document.readyState") == "complete"
        
        i = 0
        while i<15:
            if not wait_for_page():
                time.sleep(.2)
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            i += 1



        div_content_list = self.load_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#list-view-2')))

        #WebDriverWait Object to act within the div_content_list
        content_list_load_wait = WebDriverWait(div_content_list,60)

        time.sleep(5)
        #grab all articles tags
        articles = content_list_load_wait.until(EC.presence_of_all_elements_located((By.TAG_NAME,'article')))
            
        print("Articles :" + str(len(articles)))

        #==========Test grabbing content from articles before putting it in a loops=============#

        #//*[@id="jsid-post-a1PBOvR"]/header/div/div[2]/div/a

        scroll_position = self.driver.find_element(By.XPATH,'//*[@id="main"]/div[1]/div/div/div/div[2]/h2')
        self.driver.execute_script("arguments[0].scrollIntoView({ block: 'start', inline: 'nearest', behavior: 'smooth' });",scroll_position)


        for x in range(number_of_posts):
            print("============================================================================")
            try:
                time.sleep(1)

                article_1 = articles[x]

                this_id = article_1.get_attribute('id')

                if this_id == "":
                    print("Somethings Wrong I can feel it")
                    continue

                xpath_string = '//*[@id="'+str(this_id)+'"]/header/div/div[2]/div/a'

                print(xpath_string)
                
                post_title_xpath= '//*[@id="'+ this_id+'"]/header/a/h2'

                post_title = self.driver.find_element(By.XPATH,post_title_xpath).text

                print(post_title)
                
                time.sleep(.1)

                dots = article_1.find_element(By.XPATH,xpath_string)

                window_height = self.driver.execute_script("return window.innerHeight;")

                scroll_position = dots.location['y'] - window_height + 150

                print("Scroll Position: " + str(scroll_position))

                self.driver.execute_script("window.scrollTo(0,{});".format(scroll_position))
                time.sleep(1)

                # Click the element
                genre_xpath = '//*[@id="'+this_id+'"]/header/div/div[1]/div[1]/div/a[2]'
                genre = self.driver.find_element(By.XPATH,genre_xpath)
                print("--------------------" + genre.text+ "--------------" )
                post_genre = genre.text

                dots.click()

                download_btn_XPATH = '//*[@id="'+ this_id +'"]/header/div/div[2]/div[2]/ul/li[1]'
                
                print(download_btn_XPATH)
                download_btn =  self.load_wait.until(EC.visibility_of_element_located((By.XPATH,download_btn_XPATH)))

                print(download_btn.text)
            
                if download_btn.text == "Download media":
                        download_btn.click()
                       
                        #print(file_name)
                        
                        #print(post_path)
                        todays_date = date.today()
                        hard_code_genre = 'meme'
                        post_status = False
                        #print(todays_date)
                        tags_string = ""

                        file_type = ""


                        try:
                            tags_xpath = '//*[@id="' + this_id +'"]/div[2]'
                            tags_section = self.load_wait.until(EC.visibility_of_element_located((By.XPATH,tags_xpath)))
                            window_height = self.driver.execute_script("return window.innerHeight;")
                            scroll_position = tags_section.location['y'] - window_height + 150
                            self.driver.execute_script("window.scrollTo(0,{});".format(scroll_position))
                            tags_list =  tags_section.find_elements(By.TAG_NAME,'a')
                            print("tags = " + str(len(tags_list)))

                            if tags_list:
                                for y in range(len(tags_list)):
                                    tags_string += "#" + tags_list[y].text + " "
                                #print(tags_string)
                            file_name = DataManagement.get_file_name(self.download_dir)
                            
                            post_path = self.download_dir +  '\\' + file_name

                            if post_path.endswith(".mp4"):
                             file_type = "video"
                            else:
                                file_type = "photo"


                            DataManagement.insertPost(post_path,post_title,post_genre,tags_string, post_status,todays_date,file_type)
                        except Exception as e:
                            print("Inner Loop bitchass: " + e)
                       
                        




                else: 
                    continue
                
            
                print(str(x))
            
                
            except KeyboardInterrupt:
                print("Good Bye")
            
                self.driver.quit()
            
                break
            
            except Exception as e:
                print("Outer Loope Error: " + e)
                
        
            except:
                print("===============================\nskipping a problematic html article code block... moving  \n=======================================")
            finally:
                print("============================================================================")
                continue
    

    def get_content_by_search(self,search_genre = 'meme', number_of_posts = 10):
                
        #open wepage
        self.driver.get("https://9gag.com/")


        #close pop-up if it shows up
        #Deal with occasional pop-up when opening the site
        try:
            self.driver.find_element_by_xpath('//*[@id="jsid-app"]/div/div[2]/div/div[1]/div/div[1]/div/svg').click()
            print("Closed Pop-up")
        except:
            print("No Pop Up this time")

        #web title
        print(self.driver.title)
        

        #find 9gag search icon
        search=self.driver.find_element(By.CLASS_NAME,"search")
        self.driver.execute_script("arguments[0].scrollIntoView();", search)
        search.click()

        #wait 5 seconds for search bar to pop up
        search_bar = self.load_wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="top-nav"]/div/div/div[1]/div/div/form/div[2]/input')))
        #jsid-post-aGENqDn > header > div > div.uikit-popup-menu > div > a


        #Now video tut on using search bar

        search_bar.send_keys(search_genre) #search this string

        search_suggestion = self.load_wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="top-nav"]/div/div/div[1]/div/div/section/div[2]/a[1]')))


        self.action.move_to_element(search_suggestion).perform()#This is how you hover

        top_suggestion = search_suggestion.text
        print(top_suggestion)

        search_suggestion.click()


        #get container with all of the posts


        self.load_wait.until(EC.presence_of_all_elements_located)


        height = self.driver.execute_script('return document.body.scrollHeight')

        print("height :" + str(height))


        #Use this function to make sure page is loaded
        def wait_for_page():
            return self.driver.execute_script("document.readyState") == "complete"


        i = 0
        while i<25:
            if not wait_for_page():
                time.sleep(.2)
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            i += 1



        div_content_list = self.load_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#list-view-2')))

        #WebDriverWait Object to act within the div_content_list
        content_list_load_wait = WebDriverWait(div_content_list,60)

        time.sleep(5)
        #grab all articles tags
        articles = content_list_load_wait.until(EC.presence_of_all_elements_located((By.TAG_NAME,'article')))
            
        print("Articles :" + str(len(articles)))

        #==========Test grabbing content from articles before putting it in a loops=============#

        #//*[@id="jsid-post-a1PBOvR"]/header/div/div[2]/div/a

        scroll_position = self.driver.find_element(By.XPATH,'//*[@id="main"]/div[2]/div[2]/div/div[1]')
        self.driver.execute_script("arguments[0].scrollIntoView({ block: 'start', inline: 'nearest', behavior: 'smooth' });",scroll_position)


        for x in range(number_of_posts):
            try:
                time.sleep(1)

                article_1 = articles[x]

                this_id = article_1.get_attribute('id')

                if this_id == "":
                    print("Somethings Wrong I can feel it")
                    continue

                xpath_string = '//*[@id="'+str(this_id)+'"]/header/div/div[2]/div/a'

                print(xpath_string)
                
                post_title_xpath= '//*[@id="'+ this_id+'"]/header/a/h2'

                post_title = self.driver.find_element(By.XPATH,post_title_xpath).text

                print(post_title)
                
                time.sleep(.1)

                dots = article_1.find_element(By.XPATH,xpath_string)

                window_height = self.driver.execute_script("return window.innerHeight;")

                scroll_position = dots.location['y'] - window_height + 150

                print("Scroll Position: " + str(scroll_position))

                self.driver.execute_script("window.scrollTo(0,{});".format(scroll_position))
                time.sleep(1)

                # Click the element
                dots.click()

                download_btn_XPATH = '//*[@id="'+ this_id +'"]/header/div/div[2]/div[2]/ul/li[1]'
                
                print(download_btn_XPATH)
                download_btn =  self.load_wait.until(EC.visibility_of_element_located((By.XPATH,download_btn_XPATH)))

                print(download_btn.text)
            
                if download_btn.text == "Download media":
                        download_btn.click()
                        time.sleep(.5)

                        
                        todays_date = date.today()
                        hard_code_genre = 'meme'
                        post_status = False
                        print(todays_date)
                        tags_string = ""

                        file_name = DataManagement.get_file_name(self.download_dir)
                        print(file_name)
                        post_path = self.download_dir +  '\\' + file_name
                        print(post_path)

                        file_type = ""

                        if post_path.endswith(".mp4"):
                            file_type = "video"
                        else:
                            file_type = "photo"
                        try:
                            tags_xpath = '//*[@id="' + this_id +'"]/div[2]'
                            tags_section = self.load_wait.until(EC.visibility_of_element_located((By.XPATH,tags_xpath)))
                            window_height = self.driver.execute_script("return window.innerHeight;")
                            scroll_position = tags_section.location['y'] - window_height + 150
                            self.driver.execute_script("window.scrollTo(0,{});".format(scroll_position))
                            tags_list =  tags_section.find_elements(By.TAG_NAME,'a')
                            print("tags = " + str(len(tags_list)))

                            if tags_list:
                                for y in range(len(tags_list)):
                                    original =  tags_list[y].text
                                    split_space = original.split()
                                    tag = "".join(split_space)
                                    tags_string += "#" + tag + " "
                                print(tags_string)
                        except Exception as e:
                            print("Inner Loop bitchass: " + e)
                            
                        try:

                            DataManagement.insertPost(post_path,post_title,hard_code_genre,tags_string, post_status,todays_date,file_type)
                        except Exception as a:
                            print("==99999999999999999999999999 SQL ERROR: " + str(a))
                        




                else: 
                    continue
                
            
                print(str(x))
            
                
            except KeyboardInterrupt:
                print("Good Bye")
            
                self.driver.quit()
            
                break
            
            except Exception as e:
                print("Outer Loope Error: " + e)
                
        
            except:
                print("===============================\nskipping a problematic html article code block... moving  \n=======================================")
            finally:
                continue
        

            
        