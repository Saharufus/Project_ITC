import threading
from get_soup_from_url import get_soup_from_url
import config


def get_rest_html(url, empty_list):
    """
    :param url: url of webpage
    :param empty_list: A soup object from the url page will be appended to the empty list
    """
    soup = get_soup_from_url(url)
    # driver = webdriver.Chrome()
    # driver.get(url)
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # driver.close()
    empty_list.append(soup)


def get_list_of_soups(url_list, empty_list):
    """
    :param url_list: A list of urls to extract soups from
    :param empty_list: The list will be filled with soups of the urls from url_list
    """
    thread_list = [threading.Thread(target=get_rest_html, args=(url, empty_list)) for url in url_list]
    divider = int(len(thread_list)/config.MULTITHREAD)
    for i in range(config.MULTITHREAD):
        for thread in thread_list[i*divider:(i+1)*divider]:
            thread.start()

        for thread in thread_list[i*divider:(i+1)*divider]:
            thread.join()
