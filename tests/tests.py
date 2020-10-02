import unittest
from context import programfiles
from collections import Counter
import numpy as np

class NounCategories(unittest.TestCase):
    def setUp(self):

        self._categories = {
            'bathroom': ['bathroom', 'bath'],
            'bedroom': ['bedroom'],
            'living room': ['living room', 'reception', 'reception room', 'receptions room',
            'reception area', 'reception space'],
            'property': ['apartment', 'maisonette', 'house', 'accommodation', 'home'],
            'garden': ['garden', 'yard'],
            'location': ['location']
        }
        self._noun_categories = programfiles.NounCategories(self._categories)

    def test_get_noun_categories(self):    
        self.assertIsNotNone(self._noun_categories.get_categories())
        self.assertEqual(type(self._noun_categories.get_categories()), dict)
        self.assertDictEqual(self._noun_categories.get_categories(), self._categories)

class TestProperty(unittest.TestCase):
    
    def setUp(self):

        self._categories = {
            'bathroom': ['bathroom', 'bath'],
            'bedroom': ['bedroom'],
            'living room': ['living room', 'reception', 'reception room', 'receptions room',
            'reception area', 'reception space'],
            'property': ['apartment', 'maisonette', 'house', 'accommodation', 'home'],
            'garden': ['garden', 'yard'],
            'location': ['location']
        }

        self._noun_categories = programfiles.NounCategories(self._categories)
        self._txt = '''A spacious and rather elegant raised ground floor two 
                    bedroom apartment with two bathrooms (one en-suite) on this historic 
                    garden square, set within this wonderful stucco fronted property.'''

 
    def test_new_property(self):
        a_property = programfiles.Property(self._txt, "Property 1")
        self.assertEqual(a_property.get_name(), "Property 1")
        self.assertEqual(a_property.get_p_description(), self._txt)
    
    def test_set_get_categories(self):
        a_property = programfiles.Property(self._txt, "Property 1")
        a_property.set_categories(self._noun_categories)
        self.assertEqual(a_property.get_categories(), self._noun_categories)
 
class TestProperties(unittest.TestCase):
    def setUp(self):

        self._categories = {
            'bathroom': ['bathroom', 'bath'],
            'bedroom': ['bedroom'],
            'living room': ['living room', 'reception', 'reception room', 'receptions room',
            'reception area', 'reception space'],
            'property': ['apartment', 'maisonette', 'house', 'accommodation', 'home'],
            'garden': ['garden', 'yard'],
            'location': ['location']
        }

        self._noun_categories = programfiles.NounCategories(self._categories)

    def test_add_properties(self):
        all_properties = programfiles.Properties()
        a_property = programfiles.Property("What a nice property", "Property 1")
        all_properties.add_property(a_property)
        self.assertEqual(all_properties.get_size(), 1)
    
    
    def test_get_properties(self):
        all_properties = programfiles.Properties()
        self.assertEqual(all_properties.get_properties(), [])

        a_property = programfiles.Property("What a nice property", "Property 1")  
        all_properties.add_property(a_property)
        self.assertEqual(all_properties.get_properties()[0], a_property)


class PropertyData(unittest.TestCase):
    def setUp(self):

        self._categories = {
            'bathroom': ['bathroom', 'bath'],
            'bedroom': ['bedroom'],
            'living room': ['living room', 'reception', 'reception room', 'receptions room',
            'reception area', 'reception space'],
            'property': ['apartment', 'maisonette', 'house', 'accommodation', 'home'],
            'garden': ['garden', 'yard'],
            'location': ['location']
        }

        self._txt = 'A wonderful apartment.'

        self._noun_categories = programfiles.NounCategories(self._categories)
        self._pos_tags = ['JJ', 'CD']
    
    def test_normalize_if_num(self):
        data = programfiles.PropertyData()
        self.assertEqual(data.normalize_if_num('two'), '2')
        self.assertEqual(data.normalize_if_num('2'), '2')

    def test_extract(self):
        a_property = programfiles.Property(self._txt, "Property 1")
        data = programfiles.PropertyData()

        data.extract(self._pos_tags, self._noun_categories, a_property)
        a_property.set_data(data)     
        self.assertEqual(a_property.get_data_content(), set([('apartment','wonderful')]))

        data = programfiles.PropertyData()
        data.extract(self._pos_tags, self._noun_categories, a_property, add_extra_nouns=True)
        a_property.set_data(data)   
        self.assertEqual(a_property.get_data_content(), set([('apartment', None),('apartment','wonderful')]))

    def test_vectorize(self):
        a_property = programfiles.Property(self._txt, "Property 1")
        data = programfiles.PropertyData()
        data.extract(self._pos_tags, self._noun_categories, a_property, add_extra_nouns=True)

        a_property.set_data(data)
        a_property.vectorize(penalty=0.5)
        vectorized_target = Counter({('apartment', None): 0.5 ,('apartment','wonderful'): 1})

        self.assertEqual(a_property.get_vectorized_data(), vectorized_target)


class TestExtractPropertyData(unittest.TestCase):

    def setUp(self):

        self._categories = {
            'bathroom': ['bathroom', 'bath'],
            'bedroom': ['bedroom'],
            'living room': ['living room', 'reception', 'reception room', 'receptions room',
            'reception area', 'reception space'],
            'property': ['apartment', 'maisonette', 'house', 'accommodation', 'home'],
            'garden': ['garden', 'yard'],
            'location': ['location']
        }

        self._noun_categories = programfiles.NounCategories(self._categories)
        self._pdata = programfiles.ExtractPropertyData('properties.txt', self._noun_categories)
        self._pos_tags = ['JJ', 'CD']
    
    def test_create_properties(self):   
        self.assertEqual(self._pdata.get_properties().get_size(), 5)
        with self.assertRaises(FileNotFoundError):
            programfiles.ExtractPropertyData('properties.tx', self._noun_categories)

    def test_get_properties(self):
        self.assertIsInstance(self._pdata.get_properties(), programfiles.Properties)

    def test_extract_property_data(self):
        self._pdata.extract(self._pos_tags, penalty=0.5)
        self._pdata.extract(self._pos_tags, penalty=0.5, add_extra_nouns=True)

        for prop in self._pdata.get_properties():
            self.assertIsNotNone(prop.get_data())
            self.assertIsNotNone(prop.get_vectorized_data())
        
      
        with self.assertRaises(TypeError):
            self._pdata.extract("A string", penalty=0.5, add_extra_nouns=True)

        with self.assertRaises(TypeError):
            self._pdata.extract(self._pos_tags, penalty='0.5', add_extra_nouns=True)
        

class TestPropertySimilarityMatrix(unittest.TestCase):

    def setUp(self):
        self._categories = {
            'bathroom': ['bathroom', 'bath'],
            'bedroom': ['bedroom'],
            'living room': ['living room', 'reception', 'reception room', 'receptions room',
            'reception area', 'reception space'],
            'property': ['apartment', 'maisonette', 'house', 'accommodation', 'home'],
            'garden': ['garden', 'yard'],
            'location': ['location']
        }
        
        self._noun_categories = programfiles.NounCategories(self._categories)
        self._pdata = programfiles.ExtractPropertyData('properties.txt', self._noun_categories)
        self._pos_tags = ['JJ', 'CD']
        self._pdata.extract(self._pos_tags, penalty=0.5)
 

    def test_build_matrix(self):
        matrix = programfiles.PropertySimilarityMatrix(self._pdata.get_properties())
        self.assertIsInstance(matrix.get_matrix(), np.ndarray)

        with self.assertRaises(TypeError):
            programfiles.PropertySimilarityMatrix('A string')

        with self.assertRaises(TypeError):
            programfiles.PropertySimilarityMatrix([])

        with self.assertRaises(TypeError):
            programfiles.PropertySimilarityMatrix(11)

if __name__ == '__main__':
    unittest.main(verbosity=2)
