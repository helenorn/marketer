from .properties import Properties
from .property import Property
from .propertyData import PropertyData
from.nounCategories import NounCategories
import re
import os.path
from os import path
from typing  import List, Dict

class ExtractPropertyData:
    
    def __init__(self, path: str, noun_categories: NounCategories):
        """Reads the inputfile with property information, creates property objects with property data.

            Variables: 
            self._document (string): the document containing property descriptions
            self._noun_categories (NounCategories): NounCategories object 
            self._properties (Properties): Properties object containing all the properties. Initially an empty Properties object.

            Parameters:
            path (string): the path to the document containing property descriptions
            noun_categories (NounCategories): NounCategories object 
        """

        self._noun_categories = noun_categories
        self._properties = Properties()
        self._document = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'documents/' + path)
        self.create_properties()

    def create_properties(self):
        """ Generates Property objects based on the input document. 
        """
    
        with open(self._document, 'r', encoding='utf8') as f:
            file_contents = f.read() 
            reg = 'Property\s*[0-9]+\s*\:'

            property_names = re.findall(reg, file_contents)
            property_text = [text for text in re.split(reg, file_contents) if text != ""]

            for i, name in enumerate(property_names):
                p = Property(property_text[i], name[:-1])
                p.set_categories(self._noun_categories)
                self._properties.add_property(p)
    

    def extract(self, pos_tags: List[str], penalty: float=0.5, add_extra_nouns: bool=False):
        """
        Extract and assigns desired data to property objects. 
        
        Parameters:
        pos_tags (list): list of tags to consider
        penalty (float): the penlaty for the noun, None touple weight
        add_extra_nouns (bool): if se to true, adds nouns of interest even without adj|num co-occurence

        """ 
        if isinstance(pos_tags, list) and all(isinstance(i, str) for i in pos_tags):
            
            for prop in self._properties:
                data = PropertyData()
                data.extract(pos_tags, self._noun_categories, prop, add_extra_nouns)
                prop.set_data(data)
                prop.vectorize(penalty)
        else:
            raise TypeError


    def get_properties(self) -> Properties:
        """ Returns:
            Properties: the object containing all the properties.
        """
        return self._properties
   

    def update(self):
        """
        Adds new properties, if any. Extracts information for new nouns and noun categories, if any.

        """
        raise NotImplementedError("You must implement the update() function in ExtractPropertyData")


    def add_nouns(self, category: str, nounlist: List[str]):
        """ Add new nouns of interest to the NounCategories object.
        
        Parameters:
        category (str): the new or existing category of the noun
        nounlist (list): a list with the nouns to be added
        """
        self._noun_categories.add_nouns(category, nounlist)
        
  
    def present_data(self):
        """ Presents the extracted data as a dictionary. 
        """
        for p in self._properties:
            show = self.generate_dictionary(p)
            print(f"\nProperty name: {p.get_name()}\n{show}")

    
    def generate_dictionary(self, prop):    
        """ Generates a dictionary of the recorded nouns and adj|num. 

        Parameters:
        prop (Property): Property-object with data
        """
        d = {}
        
        for c in self._noun_categories.get_categories():
            d[c] = {k:None for k in self._noun_categories.get_categories()[c]}

        data = prop.get_data_content()

        for items in data:
            for category in d:

                if items[0] in d[category]:
                    if d[category][items[0]]:

                        if items[1] not in d[category][items[0]] and items[1]:
                            d[category][items[0]].append(items[1])

                    elif items[1]:
                        d[category][items[0]] = [items[1]]
        return d