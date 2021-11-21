from bs4 import BeautifulSoup
from selenium import webdriver


def get_soup_from_url(url):
    """
    The function accepts a url and returned an html_text (from BeautifulSoup - html.parser) from webdriver
    :param url: url string
    :return: soup - html text (html.parser)
    """
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(30)
    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    except Exception:
        print('Site could not be reached')
        soup = None
    finally:
        driver.close()

    return soup


def main():
    driver = webdriver.Chrome()
    driver.get('https://www.tripadvisor.com/Restaurants-g293984-Tel_Aviv_Tel_Aviv_District.html')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    soup1 = get_soup_from_url('https://www.tripadvisor.com/Restaurants-g293984-Tel_Aviv_Tel_Aviv_District.html')

    assert type(soup1) == type(soup)


if __name__ == '__main__':
    main()
