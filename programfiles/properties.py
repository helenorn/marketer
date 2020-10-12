from .property import Property
from .propertiesIterator import PropertiesIterator
from typing import *

class Properties:
    def __init__(self):
        """A container for alle the Property objects. 
        """
        self.properties = []
    
    def add_property(self, new_property: Property):
        """Adds new properties.

        Parameters:
        new_property(Property): the Property object to be added. 
        """
  
        self.properties.append(new_property)
    
    def get_size(self) -> int:
        """ 
        Returns: 
        int: the lengths of the list of properties.
        """
        return len(self.properties)


    def __iter__(self):
        return PropertiesIterator(self)

        
    