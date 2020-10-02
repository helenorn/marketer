import math
from collections import Counter
import numpy as np
import seaborn as sns; sns.set_theme()
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from .properties import Properties
from.nounCategories import NounCategories
from typing import *


class PropertySimilarityMatrix:

    def __init__(self, properties: Properties):
        """Builds a similarity matrix for the given properties.

        Variables: 
        self._properties (Properties): Properties object. 
        self._size (int): number of properties contained in the properties object
        self._similarity_matrix (array): array containing the cosine similarity between the documents

        Parameters:
        properties (Properties): Properties object. 

        """
        if isinstance(properties, Properties):

            self._size = properties.get_size()
            self._similarity_matrix = []
            self._properties = properties
            self.build_matrix()
            self._similarity_matrix = np.array(self._similarity_matrix).reshape(self._size, self._size)
        
        else:
            raise TypeError

    def build_matrix(self):
        """ Builds the similarity matrix.
        """
        
        for p1 in self._properties:         
            p1 = p1.get_vectorized_data()
        
            for p2 in self._properties:
                p2 = p2.get_vectorized_data()
                v1, v2 = self.prepare_vectors(p1, p2)
                self._similarity_matrix.append(cosine_similarity([v1],[v2]))
    
                
    def prepare_vectors(self, c1: Counter, c2: Counter) -> Tuple[list, list]:
        """Prepares the vectors for each property so that they are of the same length.
        
        Parameters:
        c1 (Counter()): Counter() object with word counts for property 1
        c2 (Counter()): Counter() object with word counts for property 2
        
        Returns:
        list: list of term frequecy vectors for property 1
        list: list of term frequecy vectors for property 2
        """

        items = set(c1.keys()).union(set(c2.keys()))
     
        v1 = [c1[key] for key in items]
        v2 = [c2[key] for key in items]   

        return v1, v2

    def get_matrix(self, heatmap: bool=False) -> np.array:
        """
        Parameters:
        heatmap(bool): plots the matrix if set to True

        Returns:
        array: the similarity matrix
        """
    
        if heatmap:
            self.plot_matrix(self._similarity_matrix)

        return self._similarity_matrix

    def plot_matrix(self, matrix: np.ndarray):
        """Plots a heatmap of the similarity matrix.

        Parameters:
        matrix (array): similarity matrix to plot.

        """
        sns.heatmap(matrix, annot=True)
        plt.show()