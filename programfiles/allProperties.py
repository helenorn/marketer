from .aProperty import AProperty
from .allPropertiesIterator import AllPropertiesIterator

class AllProperties:
    def __init__(self):
        '''A container for alle the AProperty objects. 
        '''
        self._properties = []
 
    
    def add_property(self, new_property):
        '''Adds new properties.

        Parameters:
        new_property(AProperty): the AProperty object to be added. 
        '''
        try:
            assert isinstance(new_property, AProperty)

        except AssertionError:
            raise TypeError("Argument in position 1 must be AProperty-object")

        else:
            self._properties.append(new_property)
    
    def get_size(self):
        ''' 
        Returns: 
        int: the lengths of the list of properties.
        '''
        return len(self._properties)

    def get_properties(self):
        '''
        Returns:
        list: the list of properties.
        '''

        return self._properties

    def __iter__(self):
        return AllPropertiesIterator(self)

        
    