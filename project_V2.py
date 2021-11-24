from ITC_scraper_functions import *


def scrape_from_tripadvisor(city_name, file_name, pages, main_driver, threads=5):
    """Scrapes Tripadvisor restaurants in a given city and saves the data to file_name.csv"""
    main_url = get_city_rest_url(city_name, main_driver)  # a string of a url for the city page

    list_of_dicts = []
    for i in range(pages):
        main_driver.get(main_url)
        main_soup = BeautifulSoup(main_driver.page_source, 'html.parser')

        list_of_restaurants_urls = get_rest_url_list(main_soup)
        restaurant_soup_list = get_list_of_soups_main_page_url_tabs(list_of_restaurants_urls, main_driver, threads)
        list_of_dicts.extend(get_rest_details(restaurant_soup_list))

        main_url = next_page(main_soup)

    data = pd.DataFrame(list_of_dicts)
    data.to_csv(file_name + '.csv')


def scrape_list_of_cities(list_of_cities, list_of_file_names, pages, threads=5):
    options = Options()
    options.headless = True
    main_driver = webdriver.Chrome(options=options)
    for city, file in zip(list_of_cities, list_of_file_names):
        scrape_from_tripadvisor(city, file, pages, main_driver, threads)
    main_driver.quit()
