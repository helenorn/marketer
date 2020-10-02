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
    pdata.extract(penalty=0.5, pos_tags=['JJ', 'CD'])
    pdata.present_data()

    matrix = PropertySimilarityMatrix(pdata.get_properties())
    similarity = matrix.get_matrix(heatmap=False)
    print(f"\nSIMILARITY MATRIX:\n{similarity}")
    
main()