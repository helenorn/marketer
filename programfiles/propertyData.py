import nltk
from nltk import sent_tokenize, WordNetLemmatizer 
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from .nounCategories import NounCategories
from .property import Property
from typing import *
import spacy

class PropertyData:
    def __init__(self):
        """Extracts term frequency information about the description of each property.

            Variables: 
            self.data (list): stores all the registered noun-adj|num instances and their frequencies 
            self._vectorized_data (defaultdict): dictionary with vectorized data
            self._lemmatizer (WordNetlemmatizer()): lemmatizer for normalization

        """

        self.data = set()
        self._vectorized_data = None
        self._nlp = spacy.load('en_core_web_sm')
        self._lemmatizer = WordNetLemmatizer() 


    def normalize_if_num(self, num: str) -> str:
        """Given a string-representation of a number returns the numeric representation

        Parameters:
        num (str): token to convert

        Returns:
        str: numeric representation of the inputstring
        
        """

        nums_str = ['one', 'two', 'three', 'four', 'five', 'six', 'seven'
                'eight', 'nine']

        nums_int = [i+1 for i in range(9)]
        
        if num in nums_str:
            return str(nums_int[nums_str.index(num)])
        else:
            return num

            
    def vectorize(self, penalty: float=0.5) -> Counter:
            """Given a list of bigrams makes a vectorized version of the data in the list. Nouns that occour with adj|num are
            given the vector 1, nouns that appear alone are penalized . Also builds a dicitonary mapping nouns and adj|num to each category.

                Parameters:
                c (NounCategories): NounCategories object containing categories
                p (Properties): Properties objects to analyze
                penalty (float): the penlaty for the (noun, None) 

                Returns: 
                Counter: Counter object with vectorized data

            """
          
            self._vectorized_data = Counter()
            
            for bigram in self.data: 

                if bigram[1]:
                    self._vectorized_data[bigram] = 1
                else:
                    self._vectorized_data[bigram] = 1-penalty
        
            return self._vectorized_data
            
      
    def check_and_add_noun(self, ngram: str, ngram_lemma: str, token: str, token_text_lemma: str, adj_num: Any, nouns_of_interest: List[str]):
        """ Checks if an item is in the nouns of interest list and ads it if true.

        Parameters:
        ngram (str): ngram to check
        ngram_lemma (str): lemmatized version of ngram to check
        token (str): token to check
        token_text_lemma (str): lemmatized version of token to chek
        adj_num (any): NoneType-object or string with item to be added to self.data on the form (item, adj_num)
        nouns_of_interest (list): list of nouns of interest 

        """

        def check_noun(item):
            """Parameters:
            item (string): noun to be checked
            
            Returns:
            bool: True if a tuple was added, False if not
            """
            if item in nouns_of_interest:
                self.data.add((item, adj_num))
                return True
            else:
                return False

        if not check_noun(ngram) or check_noun(ngram_lemma):
            if not check_noun(token):
                check_noun(token_text_lemma)
        
        
    def extract(self, pos_tags: List[str], all_categories: NounCategories, a_property: Property, add_extra_nouns: bool=False):
        """Finds adjectives and numbers applying to nouns if interest for each property and saves them as bigrams (noun, adj|num). 

            Parameters:
            pos_tags (list): list with all desired pos-tags
            all_categories (NounCategories): NounCategories object containing categories
            a_property (Property): Property object to analyze
            add_extra_nouns (bool): if se to true, adds nouns of interest even without adj|num co-occurence

        """
    
        nouns_of_interest = [noun for nounlist in all_categories.get_categories().values() for noun in nounlist]
        document = a_property.get_p_description()
        sentences = sent_tokenize(document.lower())

        for sent in sentences:
            
            #---generate a dependecy parcing of the sentance---
            dep = self._nlp(sent)
            last = None
            ngram = ''

            for i, token in enumerate(dep):

                token_text_lemma = self._lemmatizer.lemmatize(token.text) 
                ngram_lemma = self._lemmatizer.lemmatize(ngram)

                #---add the nouns of interest to self.data if the input is True---
                if add_extra_nouns:
                    self.check_and_add_noun(ngram, ngram_lemma, token.text, token_text_lemma, None, nouns_of_interest)
               
                #---catch nouns of interest with whitespace---
                if last:
                    ngram = last + ' ' + token.text
        
                last = token.text
                possible_adj_nums = set()
                left = [token for token in dep[i].lefts]
                right = [token for token in dep[i].rights]
                possible_adj_nums = left + right
                
                #---add nouns of interest that occur with adjectives or numbers---
                for t in possible_adj_nums:
                    if t.tag_ in pos_tags:
                        adj_num = self.normalize_if_num(t.text)
                        self.check_and_add_noun(ngram, ngram_lemma, token.text, token_text_lemma, adj_num, nouns_of_interest)
         