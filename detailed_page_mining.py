import re

PRICING_RATE = 0
CUISINE = 1
CITY_RATE = 0
REMOVE_HASH = 1


def get_rest_details(soups):
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
    rest_list = []

    for soup in soups:
        try:
            name = (soup.find('div', class_="eTnlN _W w O")).find('h1', class_="fHibz").text
            rating = float(soup.find('span', class_="fdsdx").text.strip('"'))
            reviews_num = int(re.sub("[^0-9]", "", soup.find('a', class_="dUfZJ").text))
        except AttributeError:
            name = None
            rating = None
            reviews_num = None
        try:
            details = soup.find('span', class_="dyeJW VRlVV").find_all('a', class_="drUyy")
            details_list = [det.text for det in details]
            if len(details_list) == 0:
                price_rate = None
                cuisine = None
            elif '$' in details_list[PRICING_RATE]:
                price_rate = details_list[PRICING_RATE]
                if len(details_list) > 1:
                    cuisine = details_list[1:]
                else:
                    cuisine = None
            else:
                price_rate = None
                cuisine = details_list
        except AttributeError:
            price_rate = None
            cuisine = None

        try:
            city_rate = soup.find('div', class_="fYCpi").text.split()[CITY_RATE][REMOVE_HASH:]
        except AttributeError:
            city_rate = None
        try:
            address = soup.find('span', class_="brMTW").text
        except AttributeError:
            address = None
        try:
            website = soup.find('div', class_="bKBJS Me enBrh").find('a').get("href")
        except AttributeError:
            website = None
        try:
            phone = soup.find('div', class_="bKBJS Me").find('a').get("href").strip('tel:')
        except AttributeError:
            phone = None
        if not name:
            pass
        else:
            rest_dict = ({"Name": name,
                          "Rating": rating,
                          "Reviews_num": reviews_num,
                          "Price_rate": price_rate,
                          "Cuisine": cuisine,
                          "City_rate": city_rate,
                          "Address": address,
                          "Website": website,
                          "Phone": phone
                          })

            rest_list.append(rest_dict)

    return rest_list
