import argparse
import scraper
import time
from config import THREADS
import create_db


def scrape_command():
    start = time.time()
    the_parser = argparse.ArgumentParser(usage='Scrape Tripadvisor\'s restaurant info\n', allow_abbrev=False)
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
    scraper.scrape_list_of_cities(list_of_cities=args.city, pages=args.pages, threads=THREADS)
    end = time.time()
    if args.pages == 1:
        page = 'page'
    else:
        page = 'pages'
    print(f'It took {"%.2f" % (end - start)} seconds to scrape {args.pages} {page} from restaurants in {", ".join(args.city)}')


if __name__ == '__main__':
    create_db.create_db()
    scrape_command()
