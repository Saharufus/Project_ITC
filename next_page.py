def next_page(soup_of_current_page):
    """returns a soup object with the """
    page = soup_of_current_page.find('a', class_='nav next rndBtn ui_button primary taLnk')
    return 'https://www.tripadvisor.com/' + page.get('href')
