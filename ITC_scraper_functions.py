from search_in_tripadvisor import get_city_rest_url
from get_rest_url_list import get_rest_url_list
from next_page import next_page
from open_rest_in_tabs import get_list_of_soups_main_page_url_tabs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from detailed_page_mining import update_30_db
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
