import argparse
import project_V2
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from search_in_tripadvisor import get_city_rest_url

THREADS = 3


def scrape_command():
    start = time.time()
    the_parser = argparse.ArgumentParser(usage='Scrape Tripadvisor\'s restaurant info\n', allow_abbrev=False)

    the_parser.add_argument('-s',
                            '--scrape',
                            action='store_true',
                            help='''If used, scrapes from Tripadvisor. If not used,
                             gets the url of the first page of the given cities''')
    the_parser.add_argument('-c',
                            '--city',
                            required=True,
                            nargs='+',
                            help='List of cities to scrape',
                            metavar='"New York"')
    the_parser.add_argument('-f',
                            '--file_names',
                            nargs='+',
                            help='Names for the files that contain the info',
                            metavar='File-name')
    the_parser.add_argument('-p',
                            '--pages',
                            type=int,
                            help='Number of pages to scrape',
                            metavar='N')

    args = the_parser.parse_args()

    if args.file_names and len(args.city) != len(args.file_names):
        raise ValueError('files must be the equal to cities!')

    if args.scrape:
        project_V2.scrape_list_of_cities(list_of_cities=args.city,
                                         list_of_file_names=args.file_names,
                                         pages=args.pages, threads=THREADS)
        end = time.time()
        print(f'It took {"%.2f" % (end - start)} seconds to scrape {args.pages} from restaurants in {" and ".join(args.city)}')
    else:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        for city in args.city:
            print(get_city_rest_url(city, driver))


if __name__ == '__main__':
    scrape_command()
