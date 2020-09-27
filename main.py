#!/usr/bin/python
# -*- coding: utf-8 -*-
from programfiles import *
import os
from os import path

def main():
    ''' Extracts adjectives and numbers applying to a pre-defined set of nouns of interests.
        Builds a similarity matrix based on the results, and plots the matrix as a heatmap.

        Parameters:
        raw_data (bool): display data as a dictionary or as more readable text
        penalty (float): penalizes the (noun, None) instances according to input
    '''
    path = os.path.join(os.path.dirname(os.path.dirname(__file__))) + 'properties.txt'

    categories = {
        'bathroom': ['bathroom', 'bath'],
        'bedroom': ['bedroom'],
        'living room': ['living room', 'reception', 'reception room', 'receptions room',
        'reception area', 'reception space'],
        'property': ['apartment', 'maisonette', 'house', 'accommodation', 'home'],
        'garden': ['garden', 'yard'],
        'location': ['location']
    }
    
    noun_categories = NounCategories(categories)
    pdata = ExtractPropertyData(path, noun_categories)
    pdata.extract(penalty=0.5)
    pdata.present_data(raw_data=False)

    matrix = PropertySimilarityMatrix(pdata.get_properties())
    similarity = matrix.get_matrix()
    print("\nSIMILARITY MATRIX:\n", similarity)
    matrix.plot_matrix(similarity)
    
main()