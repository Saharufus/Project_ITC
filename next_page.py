def next_page(soup_of_current_page):
    """returns a url string of the next page from soup of current page"""
    page = soup_of_current_page.find('a', class_='nav next rndBtn ui_button primary taLnk')
    return 'https://www.tripadvisor.com/' + page.get('href')
