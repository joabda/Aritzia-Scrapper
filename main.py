#!/usr/bin/env python
__author__ = "Joe Abdo"
__copyright__ = "Copyright 2023"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "joe-abdo3@hotmail.com"
__status__ = "Production"

from aritziaparser  import AritziaPaser
from dotenv         import load_dotenv
from mongodb        import MongoDB_Client
from os.path        import join, dirname
from os             import environ
from scrapper       import Scrapper
import time, datetime, sched

db = MongoDB_Client("Aritzia", ["Items"])
scheduler = sched.scheduler(time.time, time.sleep)

WAIT_BETWEEN_EXECUTIONS_IN_SECONDS = environ.get("WAIT_BETWEEN_EXECUTIONS_IN_SECONDS")
if WAIT_BETWEEN_EXECUTIONS_IN_SECONDS == None:
    WAIT_BETWEEN_EXECUTIONS_IN_SECONDS = 0
WAIT_BETWEEN_EXECUTIONS_IN_SECONDS = float(WAIT_BETWEEN_EXECUTIONS_IN_SECONDS)

SAVE_HTML_TO_FILE = environ.get("SAVE_HTML_TO_FILE")
if SAVE_HTML_TO_FILE == None:
    SAVE_HTML_TO_FILE = 0
SAVE_HTML_TO_FILE = float(SAVE_HTML_TO_FILE)


def get_all_urls_to_scan() -> list[str]:
    """Function used to read all lines of a file into a list.
            Each line is an element of the list. 
            Each line a different URL that'll be used for scrapping. 

    Returns
    ----------
    List of string being the URLs.
    """
    url_file = environ.get("URL_FILE")
    if url_file == None:
        url_file = ""

    urls = []
    with open(url_file, "r", encoding="utf-8") as f:
        urls = f.readlines()
    return urls

def action(urls: list[str]) -> None:
    """Code logic, being executed every X amount of time.
    """
    global db, scheduler, WAIT_BETWEEN_EXECUTIONS_IN_SECONDS, SAVE_HTML_TO_FILE

    print("==================================================================================")
    print("Starting execution")

    for url in urls:
        print("..................................................................................")
        print(f"Reading URL {url}")

        html = ""
        try:
            html = Scrapper(url).get_html()
        except: 
            print(f"Error, invalid URL: {url}")
            continue

        try:
            if SAVE_HTML_TO_FILE:
                today = datetime.date.today().strftime("%Y-%m-%d")
                with open(f"{today}.html", "w", encoding="utf-8") as f:
                    f.write(html)
        except:
            print("Error, HTML code will not be saved to a file.")
        
        data = AritziaPaser(html).get_parsed_data()

        db.insert_and_update("Items", data)

        print(f"Next execution in {WAIT_BETWEEN_EXECUTIONS_IN_SECONDS}s")
        print("..................................................................................")
        
    scheduler.enter(WAIT_BETWEEN_EXECUTIONS_IN_SECONDS, 1, action, (get_all_urls_to_scan(), ))
    print("==================================================================================")


if __name__ == "__main__":
    # Loading .env variables
    load_dotenv(join(dirname(__file__), '.env'))
    
    # First run of the program
    action(get_all_urls_to_scan())
    
    # Starting the scheduler
    scheduler.run()
