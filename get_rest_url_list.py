import config


def get_rest_url_list(main_soup):
    """
    The function accepts a url for 30 restaurants, and returns a list of 30 urls, of each restaurant detailed page
    :param main_soup: rl for 30 restaurants
    :return: list of 30 urls
    """

    # getting the wanted card with info of the restaurants
    content = main_soup.find_all('div', class_='emrzT Vt o')

    urls = []
    for restaurant in content:
        rest_name = restaurant.find('a', class_='bHGqj Cj b').text
        if rest_name[0].isdigit():  # get rid of the sponsored
            title = restaurant.find('div', class_='OhCyu')
            rest_url = title.find("a").get("href")
            urls.append(config.MAIN_PAGE+rest_url)

    return urls
