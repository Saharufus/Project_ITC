import threading
from get_soup_from_url import get_soup_from_url


def get_rest_html(url, empty_list):
    """
    :param url: url of webpage
    :param empty_list: A soup object from the url page will be appended to the empty list
    """
    soup = get_soup_from_url(url)
    empty_list.append(soup)


def get_list_of_soups(url_list, empty_list, thread_number):
    """
    :param thread_number: The number of threads that are going to be used simultaneously
    :param url_list: A list of urls to extract soups from
    :param empty_list: The list will be filled with soups of the urls from url_list
    """
    thread_list = [threading.Thread(target=get_rest_html, args=(url, empty_list)) for url in url_list]
    for i in range(int(len(thread_list)/thread_number)):
        for thread in thread_list[i*thread_number:(i+1)*thread_number]:
            thread.start()

        for thread in thread_list[i*thread_number:(i+1)*thread_number]:
            thread.join()


def main():
    """asserts the functions"""
    soup_list = []
    url_list = ['https://www.tripadvisor.com/Restaurants-g293984-Tel_Aviv_Tel_Aviv_District.html',
                'https://www.tripadvisor.com/Restaurants-g60878-Seattle_Washington.html']
    get_list_of_soups(url_list, soup_list, 2)
    assert len(soup_list) == len(url_list)
    get_rest_html('https://www.tripadvisor.com/Restaurants-g293984-Tel_Aviv_Tel_Aviv_District.html', soup_list)
    assert len(soup_list) == len(url_list) + 1


if __name__ == '__main__':
    main()
