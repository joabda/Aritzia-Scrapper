from bs4        import BeautifulSoup
from datatypes  import AritziaItem
from datetime   import date

class AritziaPaser:
    """
    Specialized singleton parser for Aritzia clothing web page
        Parses all items with the wanted metadata and attributes.

    ...

    Attributes
    ----------
    bs4 : BeautifulSoup
        parser
    """

    def __init__(self, html: str) -> None:
        """Constructor for the class, initialized the parser to html
                and injects the HTML code to be ingested by the parser

        Parameters
        ----------
        html : str
            html code of the page to be parser
        """
        self.bs4 = BeautifulSoup(html, 'html.parser')

    def get_parsed_data(self) -> list[dict]:
        """Method that uses the injected HTML code to parse the data
                for each item. 
                Getting the name, price, brand, url and url of the image.

        Returns
        ----------
        List of all the items (in form of dictionaries) that have been parsed from the HTML code
        """
        ret: list[dict] = []

        all_items = self.bs4.findAll('div', {'class': 'product-tile'})

        today = date.today().strftime("%Y-%m-%d")
        for item in all_items:
            try:
                parsed_item = AritziaItem(
                    name=str(item.findAll(
                        'div', {'class': 'product-name'})[0].a.text.strip()),
                    url=str(item.findAll('a', {'class': 'relative'})[
                            0]["href"].strip()),
                    path=str(item.findAll(
                        'img', {"class": "w-auto"})[0]["data-original"].strip()),
                    first_seen_date=today,
                    last_seen_date=today
                )
                ret.append(parsed_item.to_document())
            except Exception as e:
                print(e)

        return ret
