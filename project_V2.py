from ITC_scraper_functions import *


def scrape_from_tripadvisor(city_name, file_name, threads=5):
    """Scrapes Tripadvisor restaurants in a given city and saves the data to file_name.csv"""
    main_url = get_city_rest_url(city_name)  # a string of a url for the city page
    main_driver = webdriver.Chrome()

    list_of_dicts = []
    for i in range(config.START_PAGE, config.END_PAGE + 1):
        main_driver.get(main_url)
        main_soup = BeautifulSoup(main_driver.page_source, 'html.parser')

        list_of_restaurants_urls = get_rest_url_list(main_soup)
        restaurant_soup_list = []
        get_list_of_soups(list_of_restaurants_urls, restaurant_soup_list, threads)
        list_of_dicts.extend(get_rest_details(restaurant_soup_list))

        main_url = next_page(main_soup)

    main_driver.quit()
    data = pd.DataFrame(list_of_dicts)
    data.to_csv(file_name + '.csv')


if __name__ == '__main__':
    scrape_from_tripadvisor('tel aviv', 'TLV_rest', threads=5)


