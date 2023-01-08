#!/usr/bin/env python
__author__ = "Joe Abdo"
__copyright__ = "Copyright 2023"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "joe-abdo3@hotmail.com"
__status__ = "Production"

from dataclasses import dataclass

@dataclass
class AritziaItem:
    """
    Data class used to represent an Aritzia item
            and the associated metadata requested.

    ...

    Attributes
    ----------
    url : str
        URL pointing to the item on Aritzia's Website
    product_name : str
        name of the product on Aritzia's website
    first_seen_date : str
        first date at which this item was seen on the Aritzia's website
    last_seen_date : str
        first date at which this item couldn't be found anymore on the Aritzia's website
    path : str
        path pointing to the location of the item's image
    """
    url: str
    name: str
    first_seen_date: str
    last_seen_date: str
    path: str

    def to_document(self) -> dict:
        """Method used convert the data class into a dictionary
                that can be inserted into a MongoDB collection
        Returns
        ----------
            A dictionary from the data class
        """
        return {
            "url": self.url,
            "name": self.name,
            "first_seen_date": self.first_seen_date,
            "last_seen_date": self.last_seen_date,
            "path": self.path
        }
