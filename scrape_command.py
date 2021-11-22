import argparse
import project_V2
import time

THREADS = 5


def scrape_command():
    start = time.time()
    the_parser = argparse.ArgumentParser(usage='Scrape Tripadvisor\'s restaurant info\n', allow_abbrev=False)

    the_parser.add_argument('-c',
                            '--city',
                            required=True,
                            nargs='+',
                            help='List of cities to scrape',
                            metavar='New York')
    the_parser.add_argument('-f',
                            '--file_names',
                            required=True,
                            nargs='+',
                            help='Names for the files that contain the info',
                            metavar='File-name')
    the_parser.add_argument('-p',
                            '--pages',
                            required=True,
                            type=int,
                            help='Number of pages to scrape',
                            metavar='N')

    args = the_parser.parse_args()

    if len(args.city) != len(args.file_names):
        raise ValueError('files must be the equal to cities!')

    project_V2.scrape_list_of_cities(list_of_cities=args.city,
                                     list_of_file_names=args.file_names,
                                     pages=args.pages, threads=THREADS)
    end = time.time()
    print(end - start)


if __name__ == '__main__':
    scrape_command()
