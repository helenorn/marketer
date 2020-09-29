from .nounCategories import NounCategories

class AProperty:

    def __init__(self, p_description, property_name):
        '''Property object that contains various information about the property.
        
        Variables:
        self._p_description (string): the raw text from the property description concering this particular property.
        self._property_name (string): the name of the property
        self._property_data (PropertyData): PropertyData objects. Initially set to None.
        self._vectorized_data (Counter): vectorized property data 
        self._categories (NounCategories): NounCategories object. Initially set to None.
    
        Parameters:
        contents (string): the raw text from the property description.
        property_name (string): the name of the property.

        '''
        self._p_description = p_description
        self._property_name = property_name
        self._property_data = None
        self._vectorized_data = None
        self._categories = None
    
    def set_data(self, data):
        '''Sets property data.

        Prameters:
        data (PropertyData): PropertyData to assign to this object.

        '''

        self._property_data = data
    
    def get_data(self):
        ''' 
        Returns:
        (PropertyData): the property data of this object
        '''
        return self._property_data

    
    def get_vectorized_data(self):
        return self._vectorized_data
    
    def set_vectorized_data(self, vectorized):
        self._vectorized_data = vectorized

    def get_data_content(self):
        '''
        Returns:
        list: the list of term frequencies for this property
            
        '''
        return self._property_data.data


    def get_name(self):
        '''
        Returns:
        string: property name
        '''
        return self._property_name

    def get_p_description(self):
        '''
        Returns:
        str: property description
        '''
        return self._p_description

    def vectorize(self, penalty):
        '''Calls the PropertyData vectorize method on the propertys data.
        '''
        try:
            assert isinstance(penalty, float)

        except AssertionError:
            raise ValueError("Argument in position 0 must be float")
        
        else:
            self._vectorized_data = self._property_data.vectorize(penalty)
        
    
    def set_categories(self, categories):
        '''Assigns categories to this object. 

        Parameters:
        NounCategories: NounCategories object that contains 
        a dictionary with categories as keys and lists of nouns of interest as values

        '''

        try:
            assert isinstance(categories, NounCategories)

        except AssertionError:
            raise TypeError("Argument in position 0 must be NounCategories-object")
        
        else:
            self._categories = categories
    
    def get_categories(self):
        '''
        Returns
        NounCategories: NounCategories object that contains 
        a dictionary with categories as keys and lists of nouns of interest as values

        '''
        return self._categories

   