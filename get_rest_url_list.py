from get_soup_from_url import get_soup_from_url

MAIN_PAGE = 'https://www.tripadvisor.com'


def get_rest_url_list(rest30_url):
    """
    The function accepts a url for 30 restaurants, and returns a list of 30 urls, of each restaurant detailed page
    :param rest30_url: rl for 30 restaurants
    :return: list of 30 urls
    """
    html_text = get_soup_from_url(rest30_url)

    # getting the wanted card with info of the restaurants
    content = html_text.find_all('div', class_='emrzT Vt o')

    urls = []
    for restaurant in content:
        rest_name = restaurant.find('a', class_='bHGqj Cj b').text
        if rest_name[0].isdigit():  # get rid of the sponsored
            title = restaurant.find('div', class_='OhCyu')
            rest_url = title.find("a").get("href")
            urls.append(MAIN_PAGE+rest_url)

    return urls



