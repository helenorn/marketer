class PropertiesIterator:
    def __init__(self, properties):
        """An iterator for the Properties object.

        Parameters:
        properties(Properties): to make the Properties objects iterable
        
        """

        self._properties = properties
        self._index = 0
        
    def __next__(self):
        if self._index < self._properties.get_size():
            result = self._properties.properties[self._index]
            self._index += 1

            return result
            
        raise StopIteration