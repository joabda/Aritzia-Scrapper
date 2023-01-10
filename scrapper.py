#!/usr/bin/env python
__author__ = "Joe Abdo"
__copyright__ = "Copyright 2023"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "joe-abdo3@hotmail.com"
__status__ = "Production"

from os                                 import environ
from PIL                                import Image
from selenium                           import webdriver
from selenium.webdriver.chrome.service  import Service
from selenium.webdriver.chrome.options  import Options
from webdriver_manager.chrome           import ChromeDriverManager
import time
import requests
import string

IMAGE_PATH=environ.get("IMAGE_STORAGE_PATH")
if IMAGE_PATH == None:
    IMAGE_PATH="./"



class Scrapper:
    """
    Class used to scrap a given URL using the selenium library
        and a chromium web driver.

    ...

    Attributes
    ----------
    driver : WebDriver
        driver used to scrap the web
    """

    def __init__(self, url: str) -> None:
        """Constructor for the class, initialized the driver
                and fetches a given URL

        Parameters
        ----------
        url : str
            url to be fetched and scraped
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options)

        if self.driver == None:
            print("Error couldn't initialize chromium web driver.")
            return
        print(f"Preparing webpage {url}")
        self.driver.get(url)
        print(f"Connection established with {url}, data is being ingested.")

    def get_html(self) -> str:
        """Method used to obtain the whole page's HTML code.
                This method will scroll the whole page till the end and obtain
                the full page source code.

        Returns
        ----------
        HTML source code as a string
        """
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(4)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight / 2);")

            # Wait to load page
            time.sleep(2)
        
        return self.driver.page_source

def format_filename(s: str) -> str:
    """Take a string and return a valid filename constructed from the string.
            Uses a whitelist approach: any characters not present in valid_chars are
            removed. Also spaces are replaced with underscores.
            
            Note: this method may produce invalid filenames such as ``, `.` or `..`
            When I use this method I prepend a date string like '2009_01_15_19_46_32_'
            and append a file extension like '.txt', so I avoid the potential of using
            an invalid filename.
    
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in s if c in valid_chars).replace(' ','_') # I don't like spaces in filenames.

def download_image(name: str, url: str) -> None:
    """Function used to download the product's image from
            it's parsed image URL.

    Parameters
    ----------
    name : str
        name of the product to which the image is being downloaded
    url : str
        url of the image to be downloaded
    """
    global IMAGE_PATH
    im = Image.open(requests.get(url, stream=True).raw)
    im.save(f"images/{format_filename(f'{name}.jpg')}")
    print(f"New image download {name} from {url}.")
