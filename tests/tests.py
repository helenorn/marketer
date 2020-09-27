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
     

class TestAProperty(unittest.TestCase):
    
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
        a_property = programfiles.AProperty(self._txt, "Property 1")
        self.assertEqual(a_property.get_name(), "Property 1")
        self.assertEqual(a_property.get_p_description(), self._txt)
    
    def test_set_get_categories(self):
        a_property = programfiles.AProperty(self._txt, "Property 1")

        with self.assertRaises(TypeError):
            a_property.set_categories("A string.")

        a_property.set_categories(self._noun_categories)
        self.assertEqual(a_property.get_categories(), self._noun_categories)
 
class TestAllProperties(unittest.TestCase):
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
        all_properties = programfiles.AllProperties()
        a_property = programfiles.AProperty("What a nice property", "Property 1")
        
        with self.assertRaises(TypeError):
            all_properties.add_property("A String")

        all_properties.add_property(a_property)
        self.assertEqual(all_properties.get_size(), 1)
    
    
    def test_get_properties(self):
        all_properties = programfiles.AllProperties()
        self.assertEqual(all_properties.get_properties(), [])

        a_property = programfiles.AProperty("What a nice property", "Property 1")  
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
    
    def test_normalize_if_num(self):
        data = programfiles.PropertyData()
        self.assertEqual(data.normalize_if_num('two'), '2')
        self.assertEqual(data.normalize_if_num('2'), '2')

    def test_extract(self):
        a_property = programfiles.AProperty(self._txt, "Property 1")
        data = programfiles.PropertyData()

        with self.assertRaises(ValueError):
            data.extract("A string", a_property)

        with self.assertRaises(ValueError):
            data.extract(self._noun_categories, data)

        data.extract(self._noun_categories, a_property)
        a_property.set_data(data)     
        self.assertEqual(a_property.get_data_content(), set([('apartment', None),('apartment','wonderful')]))

    def test_vectorize(self):
        a_property = programfiles.AProperty(self._txt, "Property 1")
        data = programfiles.PropertyData()
        data.extract(self._noun_categories, a_property)
        a_property.set_data(data)

        with self.assertRaises(ValueError):
            a_property.vectorize(penalty="hei")

        a_property.vectorize(penalty=0.5)
        vectorized_target = Counter({('apartment', None): 0.5 ,('apartment','wonderful'): 1})
        self.assertEqual(a_property.get_vectorized_data(), vectorized_target)
   
    def present_data(self):
        pass


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

    def test_create_properties(self):

        with self.assertRaises(FileNotFoundError):
            programfiles.ExtractPropertyData('properties.tx', self._noun_categories)
        
        self.assertEqual(self._pdata.get_properties().get_size(), 5)
    
    def test_get_properties(self):
        self.assertIsInstance(self._pdata.get_properties(), programfiles.AllProperties)

    def test_extract_property_data(self):
        self._pdata.extract(penalty=0.5)
        for prop in self._pdata.get_properties():
            self.assertIsNotNone(prop.get_data())
            self.assertIsNotNone(prop.get_vectorized_data())
        
    def test_present_data(self):
        self._pdata.extract(penalty=0.5)

        with self.assertRaises(ValueError):
            self._pdata.present_data(raw_data='Hello')
    
  
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
        self._pdata.extract(penalty=0.5)
 

    def test_build_matrix(self):

        all_properties = programfiles.AllProperties() 
        a_property = programfiles.AProperty("A wonderful garden", "Property 1")
        all_properties.add_property(a_property)
        
        with self.assertRaises(ValueError):
            programfiles.PropertySimilarityMatrix('A String.') 

        with self.assertRaises(ValueError):
            programfiles.PropertySimilarityMatrix(all_properties) 

        matrix = programfiles.PropertySimilarityMatrix(self._pdata.get_properties())
        self.assertIsInstance(matrix.get_matrix(), np.ndarray)


if __name__ == '__main__':
    unittest.main(verbosity=2)
