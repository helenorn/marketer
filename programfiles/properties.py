from .property import Property
from .propertiesIterator import PropertiesIterator
from typing import *

class Properties:
    def __init__(self):
        """A container for alle the Property objects. 
        """
        self._properties = []
    
    def add_property(self, new_property: Property):
        """Adds new properties.

        Parameters:
        new_property(Property): the Property object to be added. 
        """
  
        self._properties.append(new_property)
    
    def get_size(self) -> int:
        """ 
        Returns: 
        int: the lengths of the list of properties.
        """
        return len(self._properties)

    def get_properties(self) -> List[Property]:
        """
        Returns:
        list: the list of properties.
        """
        return self._properties

    def __iter__(self):
        return PropertiesIterator(self)

        
    