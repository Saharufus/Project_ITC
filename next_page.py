import config


def next_page(soup_of_current_page):
    """
    @param soup_of_current_page: a html soup of restaurants page
    @return: url string of the next page from soup of current page
    """
    page = soup_of_current_page.find('a', class_='nav next rndBtn ui_button primary taLnk')
    return config.MAIN_PAGE + page.get('href')

