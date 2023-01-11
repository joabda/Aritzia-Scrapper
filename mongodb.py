#!/usr/bin/env python
__author__ = "Joe Abdo"
__copyright__ = "Copyright 2023"
__credits__ = [
    "https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python"]
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "joe-abdo3@hotmail.com"
__status__ = "Production"

from datetime   import date
from os         import environ
from pymongo    import MongoClient
from scrapper   import download_image
from singleton  import singleton


@singleton
class MongoDB_Client:
    """
    A singleton class used to manipulate MongoDB NonSQL Databases.

    ...

    Attributes
    ----------
    db_name : str
        name of the database being worked on
    client : MongoClient
        database handler for mongodb
    """

    def __init__(self, db_name: str, collections: list[str]) -> None:
        """Constructor for the class, initialized the database if it doesn't exist
                and verifies the collection existence.

        Parameters
        ----------
        db_name : str
            name of the database to be used
        collections : list
            list of the collection names that should be available in this database
        """

        self.client = MongoClient(environ.get("MONGODB_URL"))
        self.db_name = db_name

        if self.db_name not in self.client.list_database_names():
            print(
                f"Database {self.db_name} didn't previously exist, creating now....")
        self.database = self.client[self.db_name]

        existing_collections = self.database.list_collection_names()
        for collection in collections:
            if collection not in existing_collections:
                print(
                    f"Collection {collection} didn't previously exist in database {self.db_name}, creating now....")
                self.database.create_collection(collection)

        print(f"Successfully initialized a connection with {self.db_name} DB.")

    def insert_and_update(self, collection: str, documents: list[dict]) -> bool:
        """Method used to insert document(s) into a specific collection
                if these documents don't already exist in that collection. 
                This method will also update existing documents and change their last seen documents
                if they've been found in the HTML code but already exist in the database
                their last seen date will be update to the current date.

        Parameters
        ----------
        collection : str
            name of the collection in which the insertion should happen
        documents : list
            list of the documents (dictionaries) of any kind to be treated 
                these are all the found documents in the HTML code

        Returns
        ----------
            True if the insertion & update were both successful,
            False if any one of insert or update operations failed.
        """
        to_update = []
        to_insert = []

        for doc in documents:
            if self.exists(collection, "name", doc["name"]):
                to_update.append(doc)
            else:
                to_insert.append(doc)

        ret_update = self.update(
            collection, to_update, "last_seen_date", date.today().strftime("%Y-%m-%d"))
        ret_insert = self.insert(collection, to_insert)

        return ret_update and ret_insert

    def insert(self, collection: str, documents: list[dict]) -> bool:
        """Method used to insert document(s) into a specific collection
                of the previously initialized database. 
                When a new item is to be inserted, then it's image is to be
                downloaded from it's URL.

        Parameters
        ----------
        collection : str
            name of the collection in which the insertion should happen
        documents : list
            list of the documents (dictionaries) of any kind to be inserted into the collection

        Returns
        ----------
            True if the insertion was successful,
            False if any one document couldn't be inserted.
        """
        ret = True
        number_of_documents = len(documents)
        number_of_documents_inserted = 0

        for doc in documents:
            try:
                print(f"#{number_of_documents_inserted} Successfully inserted {doc['name']}")
                self.database[collection].insert_one(doc)
                download_image(doc["name"], doc["path"])
                number_of_documents_inserted += 1
            except:
                print(f"Error with product {doc['name']}")

        ret = number_of_documents_inserted == number_of_documents
        
        if ret:
            print(f"Successfully inserted #{number_of_documents} document " +
                  f"into {self.db_name}.{collection}")
        else:
            print(f"Error inserting, only #{number_of_documents_inserted} " +
                  f"of {number_of_documents} document were inserted into "
                  f"{self.db_name}.{collection}")

        return ret

    def update(self, collection: str, documents: list[dict], attribute: str, new_value: str) -> bool:
        """Method used to update document(s) from a specific collection
                of the previously initialized database. 
                Using the name to find a document the method will update 
                a certain attribute to a new given value

        Parameters
        ----------
        collection : str
            name of the collection in which the update should happen
        documents : list
            list of the documents (dictionaries) of any kind to be update in the collection
        attribute : str
            name of attribute from the document that should be update
        new_value : str
            new value to be given to the attribute

        Returns
        ----------
            True if the update was successful for all the elements,
            False if any one document couldn't be updated.
        """
        ret = True
        number_of_documents = len(documents)
        number_of_documents_updated = 0

        if number_of_documents > 0:
            for doc in documents:
                query_count = self.database[collection].update_one(
                    {"name": doc["name"]}, {"$set": {attribute: new_value}}).matched_count
                ret |= query_count == 1
                number_of_documents_updated += query_count

        if ret:
            print(f"Successfully updated #{number_of_documents} document " +
                  f"in {self.db_name}.{collection}")
        else:
            print(f"Error inserting, only #{number_of_documents_updated} " +
                  f"of {number_of_documents} document were updated in "
                  f"{self.db_name}.{collection}")

        return ret

    def exists(self, collection: str, id_attribute: str, id: str) -> bool:
        """Method used to check if a certain item exists in the database
                and collection desired.

        Parameters
        ----------
        collection : str
            name of the collection in which the insertion should happen
        id_attribute : str
            attribute of the document that we should match the value against
        id : str
            value that we are searching for in a specific attribute

        Returns
        ----------
            True if the item exists in the collection,
            False if it doesn't.
        """
        return len(list(self.database[collection].find(({id_attribute: id})))) > 0
