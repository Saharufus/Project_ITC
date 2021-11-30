import re
from update_db import TableUpdate
import config
from datetime import datetime
from config import PRICING_RATE, CUISINE, CITY_RATE, REMOVE_HASH, NUM_TO_DIVIDE_RATING


class RestaurantSoup:
    def __init__(self, soup):
        self.soup = soup

    def get_name(self):
        try:
            name = (self.soup.find('div', class_="eTnlN _W w O")).find('h1', class_="fHibz").text
        except AttributeError:
            name = None
        return name

    def get_rating(self):
        try:
            rating = float(self.soup.find('span', class_="fdsdx").text.strip('"'))
        except AttributeError:
            rating = None
        return rating

    def get_reviews_num(self):
        try:
            reviews_num = int(re.sub("[^0-9]", "", self.soup.find('a', class_="dUfZJ").text))
        except AttributeError:
            reviews_num = None
        return reviews_num

    def get_cuisine_and_price(self):
        try:
            details = self.soup.find('span', class_="dyeJW VRlVV").find_all('a', class_="drUyy")
            details_list = [det.text for det in details]
            if len(details_list) == 0:
                price_rate = None
                cuisine = None
            elif '$' in details_list[PRICING_RATE]:
                price_rate = details_list[PRICING_RATE]
                if len(details_list) > 1:
                    cuisine = details_list[CUISINE:]
                else:
                    cuisine = None
            else:
                price_rate = None
                cuisine = details_list
        except AttributeError:
            price_rate = None
            cuisine = None
        return cuisine, price_rate

    def get_city_rate(self):
        try:
            city_rate = self.soup.find('div', class_="fYCpi").text.split()[CITY_RATE][REMOVE_HASH:]
        except AttributeError:
            city_rate = None
        return city_rate

    def get_address(self):
        try:
            address = self.soup.find('span', class_="brMTW").text
        except AttributeError:
            address = None
        return address

    def get_website(self):
        try:
            website = self.soup.find('div', class_="bKBJS Me enBrh").find('a').get("href")
        except AttributeError:
            website = None
        return website

    def get_phone(self):
        try:
            phone = self.soup.find('div', class_="bKBJS Me").find('a').get("href").strip('tel:')
        except AttributeError:
            phone = None
        return phone

    def get_reviews(self):
        """
        @param soup: html text from tripadvisor website
        @return: dictionary with all reviews on html, keys: id, title, user_id, text( review content), rating, date
        """
        comments = self.soup.findAll('div', class_="reviewSelector")
        reviews_list = []
        for comment in comments:
            review_dict = {}
            review_dict['review_title'] = comment.find('span', class_='noQuotes').text
            review_dict['rev_id'] = comment.get('data-reviewid')
            review_dict['review_text'] = comment.find('p', class_='partial_entry').text[:255]
            date = comment.find('span', class_='ratingDate').get('title')
            review_dict['date'] = datetime.strptime(date, '%B %d, %Y')
            review_dict['user_name'] = comment.find('div', class_="info_text pointer_cursor").text
            rating = comment.find('div', class_="ui_column is-9").find('span')
            review_dict['rate'] = int(int(rating['class'][1].split('_')[1]) / NUM_TO_DIVIDE_RATING)
            reviews_list.append(review_dict)
        return reviews_list


def update_table_in_db(soup, city_name):
    """
    Gets a soup objet of a restaurant webpage from Tripadvisor and returns the details of the restaurant in a dictionary
    :param soup: soup object of restaurant webpage
    :return: dictionary: {'name': name_of_rest, 'rating': rating_of_rest,...}
    """
    rest = RestaurantSoup(soup)
    name = rest.get_name()
    if name:
        cuisine, price_rate = rest.get_cuisine_and_price()
        details = [name,
                   city_name,
                   rest.get_rating(),
                   rest.get_reviews_num(),
                   price_rate,
                   rest.get_city_rate(),
                   rest.get_address(),
                   rest.get_website(),
                   rest.get_phone()]
        rest_dict = dict(zip(config.RESTAURANTS_COLS, details))
        res_table = TableUpdate(name='restaurants',
                                data=rest_dict,
                                connection=config.CONNECTION)
        res_table.insert_table()
        res_id = res_table.get_last_res_id()
        if cuisine:
            for cuis in cuisine:
                data = dict(zip(config.CUISINES_COLS, [res_id, cuis]))
                cuis_table = TableUpdate(name='cuisines',
                                         data=data,
                                         connection=config.CONNECTION)
                cuis_table.insert_table()

        reviews = rest.get_reviews()
        for review in reviews:
            review.update({'res_id': res_id})
            rev_table = TableUpdate(name='reviews', data=review, connection=config.CONNECTION)
            rev_table.insert_table()


    else:
        pass


def get_reviews_from_soup(soup):
    """
    @param soup: html text from tripadvisor website
    @return: dictionary with all reviews on html, keys: id, title, user_id, text( review content), rating, date
    """
    comments = soup.findAll('div', class_="reviewSelector")
    reviews_list = []
    for comment in comments:
        review_dict = {}
        review_dict['review_title'] = comment.find('span', class_='noQuotes').text
        review_dict['rev_id'] = comment.get('data-reviewid')
        review_dict['review_text'] = comment.find('p', class_='partial_entry').text
        date = comment.find('span', class_='ratingDate').get('title')
        review_dict['date'] = datetime.strptime(date, '%B %d, %Y')
        review_dict['user_name'] = comment.find('div', class_="info_text pointer_cursor").text
        rating = comment.find('div', class_="ui_column is-9").find('span')
        review_dict['rate'] = int(int(rating['class'][1].split('_')[1]) / NUM_TO_DIVIDE_RATING)
        reviews_list.append(review_dict)
    return reviews_list

def update_30_db(soups, city_name):
    """
    The function accepts a list of soups (html text) of detailed restaurant pages
    and return a list of dictionaries. Each dictionary contains details on restaurant
    :param soups: list of BeautifulSoup object (html text)
    :return: list of restaurant details dictionaries, as described bellow:
    dict items: Name(str, restaurant name), Rating(float, restaurant rating between 1-5), Reviews_num(int, the number of
    reviewers), Price_rate(str of $, representing the price rate), Cuisine(str, restaurant cuisine), separate by comma),
    City_rate(int, the rate of the restaurant among all the city's restaurants), Address(str, restaurant address),
    Website(str, url to the restaurant website), Phone(str, restaurant phone-number)
    """
    for soup in soups:
        update_table_in_db(soup, city_name)
