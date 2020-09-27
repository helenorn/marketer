
class AllPropertiesIterator:
    def __init__(self, all_properties):
        '''An iterator for the AllProperties object.

        Parameters:
        all_properties (AllProperties): AllProperties to make iterable
        
        '''
        self._all_properties = all_properties
        self._index = 0
    
    def __next__(self):
        if self._index < self._all_properties.get_size():
            result = self._all_properties.get_properties()[self._index]
            self._index += 1

            return result
            
        raise StopIteration