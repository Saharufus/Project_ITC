import argparse
import scraper
import time
from config import THREADS
from create_db import create_db
import logging
import API_scraper
import pymysql

logging.basicConfig(filename='Tripadvisor scraper log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s', filemode='w')


def scrape_command():
    start = time.time()
    the_parser = argparse.ArgumentParser(usage='Scrape Tripadvisor\'s restaurant info\n', allow_abbrev=False)
    the_parser.add_argument('--API',
                            action='store_true',
                            help='Scrape data from API')
    the_parser.add_argument('-c',
                            '--city',
                            required=True,
                            nargs='+',
                            help='List of cities to scrape',
                            metavar='"New York"')
    the_parser.add_argument('-p',
                            '--pages',
                            required=True,
                            type=int,
                            help='Number of pages to scrape',
                            metavar='N')
    args = the_parser.parse_args()
    if args.API:
        API_scraper.scrape_cities_API(list_of_cities=args.city, num_rests=args.pages)
    else:
        scraper.scrape_list_of_cities(list_of_cities=args.city, pages=args.pages, threads=THREADS)
    end = time.time()
    if args.pages == 1:
        page = 'page'
    else:
        page = 'pages'
    logging.info(f'It took {"%.2f" % (end - start)} seconds to scrape {args.pages} {page} from restaurants in\
{", ".join(args.city)}')


if __name__ == '__main__':
    try:
        create_db()
        scrape_command()
    except pymysql.err.OperationalError:
        err = 'Create DB Error: Connection to MySQL server failed, please check your credentials'
        logging.error(err)
        print(err)
