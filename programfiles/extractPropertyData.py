from .allProperties import AllProperties
from .aProperty import AProperty
from .propertyData import PropertyData
import re
import os.path
from os import path


class ExtractPropertyData:
    
    def __init__(self, path, noun_categories):
        '''Reads the inputfile with property information, creates property objects with property data.

            Variables: 
            self._document (string): the document containing property descriptions
            self._noun_categories (dict): cictionary on the form categories: [nouns of interest]
            self._properties (AllProperties): AllProperties object containing all the properties. Initially an empty AllProperties object.

            Parameters:
            path (string): the path to the document containing property descriptions
            noun_categories (dict): cictionary on the form categories: [nouns of interest]
        '''

        self._noun_categories = noun_categories
        self._properties = AllProperties()
        self._document = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'documents/' + path)

        self.create_properties()


   
    def create_properties(self):
        ''' Generates AProperty objects based on the input document. 
        '''
        try:     
            open(self._document, 'r', encoding='utf8')
            
        except FileNotFoundError:
            raise

        try:
            f = open(self._document, 'r', encoding='utf8')
            file_contents = f.read() 
            
            assert os.path.getsize(self._document) > 0

        except ValueError:
            raise ValueError("Document can not be empty.")
        
        else:
            with open(self._document, 'r', encoding='utf8') as f:
                file_contents = f.read() 
                reg = 'Property\s*[0-9]+\s*\:'

                property_names = re.findall(reg, file_contents)
                property_text = [text for text in re.split(reg, file_contents) if text != ""]

                for i, name in enumerate(property_names):
                    p = AProperty(property_text[i], name[:-1])
                    p.set_categories(self._noun_categories)
                    self._properties.add_property(p)
        

        
    def extract(self, penalty=0.5):
        '''
        Extract and assigns desired data to property objects. 
        
        Parameters:
        penalty (float): the penlaty for the noun, None touple weight


        ''' 
        
        try:
            assert self._properties.get_size() > 0

        except AssertionError:
            raise ValueError("Empty property list")

        else:
            for prop in self._properties:
                data = PropertyData()
                data.extract(self._noun_categories, prop)
                prop.set_data(data)
                prop.vectorize(penalty)
 

    def get_properties(self):
        ''' Returns:
            AllProperties: the object containing all the properties.
        '''
        return self._properties
   

    def update(self):
        '''
        Adds new properties, if any. Extracts information for new nouns and noun categories, if any.

        '''
        raise NotImplementedError("You must implement the update() function in ExtractPropertyData")


    def add_nouns(self, category, nounlist):
        ''' Add new nouns of interest to the NounCategories object.
        
        Parameters:
        category (str): the new or existing category of the noun
        nounlist (list): a list with the nouns to be added
        '''
        self._noun_categories.add_nouns(category, nounlist)
        

    def present_data(self, raw_data=False):
        ''' Presents the extracted data as either a dictionary or as text.¨
         
        Parameters:
        raw_data(bool): Displays dictinary when true, text otherwise. Set to false by default.
    
        '''
        try:
            assert isinstance(raw_data, bool)
        
        except AssertionError:
            raise ValueError("Invalid argument, bool expected.")
        
        else:
            for p in self._properties:

                show = {}
                
                for c in self._noun_categories.get_categories():
                    show[c] = {k:None for k in self._noun_categories.get_categories()[c]}
    
                print("\nProperty name:",p.get_name())
                
                data = p.get_data_content()

                for bigram in data:
                    for category in show:
                        if bigram[0] in show[category]:
                            if show[category][bigram[0]]:
                                    if bigram[1] not in show[category][bigram[0]] and bigram[1]:
                                        show[category][bigram[0]].append(bigram[1])
                            elif bigram[1]:
                                show[category][bigram[0]] = [bigram[1]]
                
                    
                if raw_data == True:
                    print(show)
                    print('-'*100)

                else:
                    for category in show:
                        print("\nFrequency for category:",category, ".")
                        
                        failed = []

                        for noun in show[category].items():
                            if not noun[1]:
                                failed.append(noun[0])
                            else:
                                print("Adjectives and numbers applied to '", noun[0], "'",":", noun[1])
                            
                        if failed:
                            print("The program failed to record any adjectives or numbers applied to the following nouns:")
                            print(failed)
                
                print('-'*100)