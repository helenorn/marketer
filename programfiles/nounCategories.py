
class NounCategories:
    def __init__(self, categories_dict):
        '''Stores the noun categories and nouns of interst. Gives the user the ability to 
        add noun categories if needed.

        Parameters:
        categories_dict (dict): dictionary of predefined categories and nouns of interest
        '''
        self._categories_dict = categories_dict

    def add_noun(self, category, new_nouns):
        ''' Add new nouns of interest to the NounCategories object.
        
        Parameters:
        category (str): the new or existing category of the noun
        new_nouns (list): a list with the nouns to be added
        '''

        raise NotImplementedError("You must implement the add_noun() function in NounCategories")

    def get_categories(self):
        '''
        Returns:
        dict: dictionary with all categories
        '''
        return self._categories_dict
