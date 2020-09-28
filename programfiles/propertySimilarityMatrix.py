import math
from collections import Counter
import numpy as np
import seaborn as sns; sns.set_theme()
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from .allProperties import AllProperties

class PropertySimilarityMatrix:

    def __init__(self, properties):
        '''Builds a similarity matrix for the given properties.

        Variables: 
        self._properties (AllProperties): AllProperties object. 
        self._size (int): number of properties contained in the properties object
        self._similarity_matrix (array): array containing the cosine similarity between the documents

        Parameters:
        properties (AllProperties): AllProperties object. 

        '''
        try:
            assert isinstance(properties, AllProperties)

        except AssertionError:
            raise ValueError("Input must be AllProperties object")

        else:
            self._properties = properties
            self._size = properties.get_size()
            self._similarity_matrix = []
        
        try:
            assert self._size >= 2

        except AssertionError:
            raise ValueError("Property list must have length >= 2")
        
        else:
            try:
                for p in self._properties:
                    assert p.get_vectorized_data()
                    assert isinstance(p.get_vectorized_data(), Counter)

            except AssertionError:
                raise ValueError("Property data must be vectorized")
        
            else:
                self.buildMatrix()
                self._similarity_matrix = np.array(self._similarity_matrix).reshape(self._size, self._size)


    def buildMatrix(self):
        ''' Builds the similarity matrix.
        '''
        
        for p1 in self._properties:         
            p1 = p1.get_vectorized_data()
        
            for p2 in self._properties:
                p2 = p2.get_vectorized_data()
                v1, v2 = self.prepareVectors(p1, p2)
                self._similarity_matrix.append(cosine_similarity([v1],[v2]))
    
                
    def prepareVectors(self, c1, c2):
        '''Prepares the vectors for each property so that they are of the same length.
        
        Parameters:
        c1 (Counter()): Counter() object with word counts for property 1
        c2 (Counter()): Counter() object with word counts for property 2
        
        Returns:
        list: list of term frequecy vectors for property 1
        list: list of term frequecy vectors for property 2
        '''

        items = set(c1.keys()).union(set(c2.keys()))
     
        v1 = [c1[key] for key in items]
        v2 = [c2[key] for key in items]   

        return v1, v2

    def get_matrix(self, heatmap=False):
        '''
        Returns:
        array: the similarity matrix
        '''
        try:
            assert isinstance(heatmap, bool)

        except AssertionError:
            raise ValueError("Invalid argument, argument must be bool")

        else:
            if heatmap:
                self.plot_matrix(self._similarity_matrix)

        return self._similarity_matrix

    def plot_matrix(self, matrix):
        '''Plots a heatmap of the similarity matrix.

        Parameters:
        matrix (array): similarity matrix to plot.

        '''
        try:
            assert isinstance(matrix, np.ndarray)

        except AssertionError:
            raise ValueError("Invalid argument, argument must be numpy array")

        else:
            sns.heatmap(matrix, annot=True)
            plt.show()