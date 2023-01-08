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
        counter = 0
        while True and counter < 5:
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
            counter += 1

        counter *= 2
        return self.driver.page_source

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
    im.save(f"images/{name}.jpg")
    print(f"New image download {name} from {url}.")