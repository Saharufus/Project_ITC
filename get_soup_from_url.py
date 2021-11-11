from bs4 import BeautifulSoup
from selenium import webdriver


def get_soup_from_url(url):
    """
    The function accepts a url and returned an html_text (from BeautifulSoup - html.parser) from webdriver
    :param url: url string
    :return: soup - html text (html.parser)
    """
    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    return soup
