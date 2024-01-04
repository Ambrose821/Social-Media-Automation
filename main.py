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
from Sourcer import Sourcer
from post import post
from custom_excpetions import *

#duplicate posts wityh differeny captions
source_instance = Sourcer()


post.send_post_twitter(num_posts=10)



try:
  #  source_instance.get_top_content(number_of_posts=10)
    #post.send_post_twitter(num_posts=10)
    num = input("What would you like to say?")

except Exception as e:
    print("\n Posting Error : " + str(e) + "\n")

